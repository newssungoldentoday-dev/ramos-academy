#!/usr/bin/env python3
"""
Prints a summary of lessons-url.js: how many lessons per subject/course,
and how long each course chain is.

Run:
    python3 tools/lesson-stats.py
"""

import re
import json
from collections import defaultdict

def main():
    with open("lessons-url.js") as f:
        js_text = f.read()

    match = re.search(r"const LESSONS\s*=\s*(\[.*?\]);", js_text, re.DOTALL)
    raw = match.group(1)
    raw = re.sub(r"(\w+)\s*:", r'"\1":', raw)
    raw = re.sub(r",(\s*[\]}])", r"\1", raw)
    lessons = json.loads(raw)

    by_subject = defaultdict(list)
    by_course = defaultdict(list)

    for l in lessons:
        by_subject[l["subject"]].append(l["id"])
        by_course[f'{l["subject"]} / {l["course"]}'].append(l["id"])

    print(f"Total lessons: {len(lessons)}\n")

    print("By subject:")
    for subject, ids in sorted(by_subject.items()):
        print(f"  {subject}: {len(ids)} lesson(s)")

    print("\nBy course:")
    for course, ids in sorted(by_course.items()):
        print(f"  {course}: {len(ids)} lesson(s) — {', '.join(ids)}")

if __name__ == "__main__":
    main()
