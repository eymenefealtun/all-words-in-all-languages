"""Check word lists against the rules in how_to_use/how_to_contribute_for_how_to_use.md.

Errors break a rule that holds for every language, and make the check fail.
Warnings point at entries that are often noise (numbers, symbols, phrases,
words in another script) but can be legitimate in some languages, so they
never fail the check.

Usage:
    python scripts/validate.py                              # every language
    python scripts/validate.py Turkish German               # only these
    python scripts/validate.py --changed-since origin/main  # only changed lists
"""

import argparse
import collections
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from wordlist import NON_LANGUAGE_DIRS, ROOT, load_languages, use_utf8_output, word_file

EXAMPLE_COUNT = 5
# Apostrophes, hyphens, periods and colons are left out on purpose:
# languages use them inside words (o'zbek, Tel-Aviv, E4:an).
SUSPICIOUS_PUNCTUATION = set('()[]{}<>/\\@#*_&;!?"|%')
# A script used by less than this share of the letters counts as foreign.
MINOR_SCRIPT_SHARE = 0.02
CONTROL_CHARS = re.compile(r"[\x00-\x09\x0b\x0c\x0e-\x1f\x7f-\x9f]")  # line breaks are reported on their own
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"


class Report:
    def __init__(self, path):
        self.path = path
        self.errors = []
        self.warnings = []


def examples(items, show=lambda item: f'"{shorten(item)}"'):
    shown = ", ".join(show(item) for item in items[:EXAMPLE_COUNT])
    return shown + (", ..." if len(items) > EXAMPLE_COUNT else "")


def shorten(text, limit=40):
    return text if len(text) <= limit else text[:limit] + "…"


def entries_with(text, chars):
    """Distinct stripped entries that contain any of chars, in file order."""
    if not chars:
        return []
    char_class = "".join(re.escape(c) for c in sorted(chars))
    # The lookbehind anchors matches to entry starts, which keeps the scan linear.
    found = re.findall(f"(?<![^,\r\n])[^,\r\n]*[{char_class}][^,\r\n]*", text)
    return list(dict.fromkeys(entry.strip() for entry in found))


def script_of(char):
    name = unicodedata.name(char, "").removeprefix("HALFWIDTH ").removeprefix("FULLWIDTH ")
    if name.startswith("CJK"):
        return "CJK"
    # "KATAKANA-HIRAGANA PROLONGED SOUND MARK" belongs to katakana.
    script = name.split(" ", 1)[0].split("-", 1)[0]
    # Modifier letters (Hawaiian ʻokina) and combining marks belong to no script.
    return None if script in ("", "MODIFIER", "COMBINING") else script


def check_file(name):
    path = word_file(name)
    report = Report(path.relative_to(ROOT).as_posix())
    raw = path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        report.errors.append("the file starts with a byte order mark (BOM); save it as UTF-8 without BOM")
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        report.errors.append(f"the file is not valid UTF-8 (first bad byte at offset {e.start})")
        return report

    entries = text.split(",")
    words = [entry.strip() for entry in entries if entry.strip()]
    if not words:
        report.errors.append("the file has no words")
        return report
    char_counts = collections.Counter(text)

    line_breaks = char_counts["\n"] + char_counts["\r"] - text.count("\r\n")
    if line_breaks:
        report.errors.append(f"{line_breaks} line break(s); all words must be on a single line")

    # Not stripped: strip() would remove the very control characters to show.
    controls = list(dict.fromkeys(
        re.findall(rf"(?<![^,\r\n])[^,\r\n]*{CONTROL_CHARS.pattern}[^,\r\n]*", text)))
    if controls:
        report.errors.append(f"{len(controls)} entries contain invisible control characters such as tabs: "
                             f"{examples(controls, show=repr)}")

    if "\ufffd" in char_counts:
        broken = entries_with(text, {"\ufffd"})
        report.errors.append(f"{len(broken)} entries contain the replacement character U+FFFD (�), "
                             f"left behind by a broken encoding conversion: {examples(broken)}")

    empty = [i for i, entry in enumerate(entries) if not entry.strip()]
    if empty:
        i = empty[0]
        context = ",".join(e.strip() for e in entries[max(0, i - 1):i + 2])
        report.errors.append(f"{len(empty)} empty entries (two commas in a row, or a comma at the start or end), "
                             f'first at entry #{i + 1}: "{shorten(context)}"')

    padded = []
    for entry in entries:
        entry = entry.replace("\r", "").replace("\n", "")
        if entry.strip() and entry != entry.strip() and not CONTROL_CHARS.search(entry):
            padded.append(entry)
    if padded:
        report.errors.append(f"{len(padded)} entries have spaces around them (no space after commas): "
                             f"{examples(padded, show=repr)}")

    counts = collections.Counter(words)
    duplicates = sorted((w for w, n in counts.items() if n > 1), key=counts.get, reverse=True)
    if duplicates:
        extra = len(words) - len(counts)
        report.errors.append(f"{extra} duplicate entries ({len(duplicates)} words appear more than once): "
                             + examples(duplicates, show=lambda w: '"%s" ×%d' % (shorten(w), counts[w])))

    # NFC is not required (Hindi lists often use precomposed nukta letters),
    # but two spellings of the same word that only differ in encoding are duplicates.
    if not unicodedata.is_normalized("NFC", text):
        forms = collections.defaultdict(list)
        for word in counts:
            forms[unicodedata.normalize("NFC", word)].append(word)
        twins = [word for word, spellings in forms.items() if len(spellings) > 1]
        if twins:
            report.errors.append(f"{len(twins)} words appear more than once, encoded with different but identical-looking "
                                 f"Unicode sequences (e.g. precomposed vs. combined vowel signs): {examples(twins)}")

    check_suspicious_entries(text, char_counts, report)
    return report


def check_suspicious_entries(text, char_counts, report):
    chars = set(char_counts)

    with_digits = entries_with(text, {c for c in chars if unicodedata.category(c) == "Nd"})
    if with_digits:
        report.warnings.append(f"{len(with_digits)} entries contain digits; often numbers or scraping noise, "
                               f"though some words are written with digits (catch-22, 第1版): {examples(with_digits)}")

    symbols = {c for c in chars
               if c != "\ufffd"  # already an error
               and (unicodedata.category(c).startswith("S")
                    or unicodedata.normalize("NFKC", c) in SUSPICIOUS_PUNCTUATION)}
    with_symbols = entries_with(text, symbols)
    if with_symbols:
        report.warnings.append(f"{len(with_symbols)} entries contain symbols or brackets that are rarely part of a word: "
                               f"{examples(with_symbols)}")

    phrases = list(dict.fromkeys(re.findall(r"(?<![^,\s])[^,\s]+(?:[^\S\r\n]+[^,\s]+)+", text)))
    if phrases:
        report.warnings.append(f"{len(phrases)} entries contain spaces; fine for multi-word expressions "
                               f"some languages list as one word: {examples(phrases)}")

    edge_hyphens = list(dict.fromkeys(
        re.findall(r"(?<![^,\r\n])[^\S\r\n]*(-[^,\r\n]*)", text)
        + re.findall(r"(?<![^,\r\n])([^,\r\n]*-)[^\S\r\n]*(?=[,\r\n]|$)", text)))
    if edge_hyphens:
        report.warnings.append(f"{len(edge_hyphens)} entries start or end with a hyphen; affixes, "
                               f"or pieces of a hyphenated word that was split: {examples(edge_hyphens)}")

    letters = collections.Counter()
    for c in chars:
        if c.isalpha() and script_of(c):
            letters[script_of(c)] += char_counts[c]
    major = {s for s, n in letters.items() if n >= MINOR_SCRIPT_SHARE * sum(letters.values())}
    minor_chars = {c for c in chars if c.isalpha() and script_of(c) and script_of(c) not in major}
    foreign = [entry for entry in entries_with(text, minor_chars)
               if not any(script_of(c) in major for c in entry if c.isalpha())]
    if foreign:
        report.warnings.append(f"{len(foreign)} entries use no {'/'.join(sorted(major))} letters, "
                               f"which most of the list is written in; possibly words from another language: "
                               f"{examples(foreign)}")


def check_structure(languages):
    problems = []
    names = [lang.get("name") for lang in languages]
    for name, count in collections.Counter(names).items():
        if count > 1:
            problems.append(f"languages.json lists {name} {count} times")
    for lang in languages:
        if not lang.get("name") or not lang.get("native"):
            problems.append(f"languages.json entry {lang} needs both a \"name\" and a \"native\" name")
        elif not word_file(lang["name"]).is_file():
            problems.append(f"{lang['name']} is listed in languages.json but {lang['name']}/{lang['name']}.txt does not exist")
    for folder in ROOT.iterdir():
        if folder.is_dir() and not folder.name.startswith(".") \
                and folder.name not in NON_LANGUAGE_DIRS and folder.name not in names:
            problems.append(f"the folder {folder.name}/ is not listed in languages.json")
    return problems


def changed_languages(ref, names):
    """Languages whose folder changed since ref, or None when that cannot be told."""
    if set(ref) == {"0"}:  # GitHub sends an all-zero ref for a newly pushed branch
        return None
    result = subprocess.run(["git", "diff", "--name-only", "-z", f"{ref}...HEAD"],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"warning: cannot diff against {ref}: {result.stderr.strip()}")
        return None
    changed = {Path(path).parts[0] for path in result.stdout.split("\0") if path}
    return [name for name in names if name in changed]


def annotate(level, path, message):
    if IN_GITHUB_ACTIONS:
        message = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{level} file={path}::{message}")


def main():
    use_utf8_output()
    parser = argparse.ArgumentParser(description="Check word lists for format problems.")
    parser.add_argument("languages", nargs="*", help="languages to check (default: all)")
    parser.add_argument("--changed-since", metavar="REF",
                        help="only check word lists changed between this git ref and HEAD")
    args = parser.parse_args()

    languages = load_languages()
    names = [lang.get("name") for lang in languages]
    failed = False

    for problem in check_structure(languages):
        print(f"error: {problem}")
        annotate("error", "languages.json", problem)
        failed = True

    if args.languages:
        unknown = [name for name in args.languages if name not in names]
        for name in unknown:
            print(f"error: {name} is not listed in languages.json")
        failed |= bool(unknown)
        targets = [name for name in args.languages if name in names]
    elif args.changed_since:
        targets = changed_languages(args.changed_since, names)
        if targets is None:
            print("Checking every word list instead.")
            targets = names
        elif not targets:
            print("No word lists changed.")
    else:
        targets = names
    targets = [name for name in dict.fromkeys(targets) if word_file(name).is_file()]

    with_errors = with_warnings = 0
    for name in targets:
        report = check_file(name)
        status = "FAIL" if report.errors else "warn" if report.warnings else "ok"
        print(f"{status:4}  {report.path}", flush=True)
        for message in report.errors:
            print(f"      error: {message}")
            annotate("error", report.path, message)
        for message in report.warnings:
            print(f"      warning: {message}")
            annotate("warning", report.path, message)
        with_errors += bool(report.errors)
        with_warnings += bool(report.warnings)

    if targets:
        print(f"\nChecked {len(targets)} word list(s): {with_errors} with errors, {with_warnings} with warnings.")
    return 1 if failed or with_errors else 0


if __name__ == "__main__":
    sys.exit(main())
