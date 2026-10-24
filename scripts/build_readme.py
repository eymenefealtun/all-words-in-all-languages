"""Regenerate the "Available Languages" table in README.md from languages.json.

The word count of a language is the number of distinct words in its list.

Usage:
    python scripts/build_readme.py           # rewrite README.md
    python scripts/build_readme.py --check   # fail if README.md is out of date
"""

import argparse
import difflib
import sys
from urllib.parse import quote

from wordlist import ROOT, load_languages, read_words, use_utf8_output, word_file

README = ROOT / "README.md"
START_MARKER = "<!-- languages:start -->"
END_MARKER = "<!-- languages:end -->"
FILE_URL = "https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/{0}/{0}.txt"


def cell(text):
    return text.replace("|", "\\|")


def languages_section():
    languages = sorted(load_languages(), key=lambda lang: lang["name"].casefold())
    lines = [
        f"## Available Languages ({len(languages)})",
        "",
        "| 🌐 Language Name | Language Native Name | Number of Words | Word File |",
        "| --- | --- | --: | --- |",
    ]
    for lang in languages:
        name = lang["name"]
        if not word_file(name).is_file():
            sys.exit(f"error: {name} is listed in languages.json but {name}/{name}.txt does not exist")
        count = len(set(read_words(name)))
        lines.append(f"| {cell(name)} | {cell(lang['native'])} | {count:,} | [Words]({FILE_URL.format(quote(name))}) |")
    return lines


def main():
    use_utf8_output()
    parser = argparse.ArgumentParser(description="Regenerate the language table in README.md.")
    parser.add_argument("--check", action="store_true", help="only report whether README.md is up to date")
    args = parser.parse_args()

    # newline="" keeps the file's own line endings.
    with open(README, encoding="utf-8", newline="") as f:
        readme = f.read()
    if START_MARKER not in readme or END_MARKER not in readme:
        print(f"error: README.md must contain {START_MARKER} and {END_MARKER} around the language table")
        return 1
    newline = "\r\n" if "\r\n" in readme else "\n"
    before, rest = readme.split(START_MARKER, 1)
    current, after = rest.split(END_MARKER, 1)
    section = newline + newline.join(languages_section()) + newline
    if section == current:
        print("README.md is up to date.")
        return 0

    if args.check:
        diff = difflib.unified_diff(current.splitlines(), section.splitlines(),
                                    "README.md", "expected", lineterm="", n=0)
        print("\n".join(diff))
        print("\nerror: README.md is out of date. Run `python scripts/build_readme.py` and commit the result.")
        return 1
    with open(README, "w", encoding="utf-8", newline="") as f:
        f.write(before + START_MARKER + section + END_MARKER + after)
    print("README.md updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
