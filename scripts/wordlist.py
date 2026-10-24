"""Shared helpers for the repository scripts."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGUAGES_FILE = ROOT / "languages.json"

# Top-level folders that are not languages.
NON_LANGUAGE_DIRS = {".git", ".github", "scripts", "how_to_use"}


def use_utf8_output():
    # Windows consoles default to a legacy code page and cannot print most scripts.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")


def load_languages():
    with open(LANGUAGES_FILE, encoding="utf-8") as f:
        return json.load(f)


def word_file(name):
    return ROOT / name / f"{name}.txt"


def read_words(name):
    """Return the non-empty, stripped entries of a word list."""
    text = word_file(name).read_bytes().decode("utf-8-sig", errors="replace")
    return [entry.strip() for entry in text.split(",") if entry.strip()]
