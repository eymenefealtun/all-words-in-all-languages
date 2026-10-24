"""Shared helpers for the repository scripts."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGUAGES_FILE = ROOT / "languages.json"

# Top-level folders that are not languages.
NON_LANGUAGE_DIRS = {"scripts", "how_to_use"}


def use_utf8_output():
    # Windows consoles default to a legacy code page and cannot print most scripts.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def load_languages():
    """Read languages.json, exiting with a readable message if it is malformed."""
    try:
        with open(LANGUAGES_FILE, encoding="utf-8") as f:
            languages = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"error: languages.json is not valid JSON: {e}")
    if not isinstance(languages, list):
        sys.exit("error: languages.json must contain a list of languages")
    for lang in languages:
        if not (isinstance(lang, dict) and is_text(lang.get("name")) and is_text(lang.get("native"))):
            sys.exit(f'error: every languages.json entry must look like {{"name": "...", "native": "..."}}, found: {lang}')
        name = lang["name"]
        if Path(name).name != name or name.startswith(".") or name in NON_LANGUAGE_DIRS:
            sys.exit(f'error: "{name}" in languages.json must be a plain folder name')
    return languages


def is_text(value):
    return isinstance(value, str) and value.strip() == value and value != ""


def word_file(name):
    return ROOT / name / f"{name}.txt"


def read_words(name):
    """Return the non-empty, stripped entries of a word list."""
    text = word_file(name).read_bytes().decode("utf-8-sig", errors="replace")
    return [entry.strip() for entry in text.split(",") if entry.strip()]
