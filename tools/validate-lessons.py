#!/usr/bin/env python3
"""
Sanity-checks lessons-url.js: duplicate ids, dangling prev/next references,
missing required fields, wrong number of options, out-of-range correct index.

Run:
    python3 tools/validate-lessons.py
"""

import re
import json
import sys

REQUIRED_FIELDS = ["id", "title", "subject", "course", "explanation", "question", "options", "correct"]

def extract_lessons_array(js_text):
    """Pulls out the LESSONS = [ ... ]; block and loosely parses it as JSON-ish."""
    match = re.search(r"const LESSONS\s*=\s*(\[.*?\]);", js_text, re.DOTALL)
    if not match:
        print("Could not find `const LESSONS = [...]` in the file.")
        sys.exit(1)

    raw = match.group(1)
    # Convert JS object syntax (unquoted keys) to valid JSON
    raw = re.sub(r"(\w+)\s*:", r'"\1":', raw)
    raw = re.sub(r",(\s*[\]}])", r"\1", raw)  # trailing commas
    raw = raw.replace("null", "null")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Could not parse LESSONS array as JSON-ish: {e}")
        print("Falling back to manual review — check formatting near that error.")
        sys.exit(1)

def main():
    path = "lessons-url.js"
    try:
        with open(path) as f:
            js_text = f.read()
    except FileNotFoundError:
        print(f"{path} not found. Run this from the repo root.")
        sys.exit(1)

    lessons = extract_lessons_array(js_text)
    ids = [l.get("id") for l in lessons]
    errors = []
    warnings = []

    # Duplicate ids
    seen = set()
    for i in ids:
        if i in seen:
            errors.append(f"Duplicate id: '{i}'")
        seen.add(i)

    for lesson in lessons:
        lid = lesson.get("id", "<missing id>")

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in lesson or lesson[field] in (None, ""):
                errors.append(f"[{lid}] missing required field: {field}")

        # Options / correct index
        options = lesson.get("options", [])
        correct = lesson.get("correct")
        if len(options) < 2:
            warnings.append(f"[{lid}] fewer than 2 answer options")
        if isinstance(correct, int) and not (0 <= correct < len(options)):
            errors.append(f"[{lid}] 'correct' index {correct} out of range for {len(options)} options")

        # prev/next point to real ids
        for key in ("prev", "next"):
            target = lesson.get(key)
            if target and target not in ids:
                errors.append(f"[{lid}] '{key}' points to unknown id: '{target}'")

    print(f"Checked {len(lessons)} lessons.\n")

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
        print(f"\n{len(errors)} error(s) found — fix before pushing.")
        sys.exit(1)
    else:
        print("No errors found. Safe to commit.")

if __name__ == "__main__":
    main()
