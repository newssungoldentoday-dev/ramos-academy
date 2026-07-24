#!/usr/bin/env python3
"""
Bulk-converts a plain text file into multiple lesson objects.
Expected format in the .txt file, one lesson per block, separated by "---":

    Title: Fractions
    Subject: Mathematics
    Course: Arithmetic
    Explanation: A fraction represents a part of a whole.
    Question: What is 1/2 + 1/4?
    Options: 1/4 | 3/4 | 2/6
    Correct: 1
    ---
    Title: Next lesson...
    ...

Run:
    python3 tools/bulk-import.py notes.txt
"""

import sys
import re

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"\s+", "-", text)

def parse_block(block):
    fields = {}
    for line in block.strip().splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        fields[key.strip().lower()] = val.strip()
    return fields

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/bulk-import.py notes.txt")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        content = f.read()

    blocks = content.split("---")
    lessons = []
    prev_id = None

    for block in blocks:
        if not block.strip():
            continue
        fields = parse_block(block)
        title = fields.get("title", "Untitled")
        slug = slugify(title)
        options = [o.strip() for o in fields.get("options", "").split("|") if o.strip()]

        lesson = {
            "id": slug,
            "title": title,
            "subject": fields.get("subject", ""),
            "subjectUrl": "subject.html",
            "course": fields.get("course", ""),
            "duration": "00:00",
            "explanation": fields.get("explanation", ""),
            "question": fields.get("question", ""),
            "options": options,
            "correct": int(fields.get("correct", 0)),
            "prev": prev_id,
            "next": None,
        }
        lessons.append(lesson)
        prev_id = slug

    for i in range(len(lessons) - 1):
        lessons[i]["next"] = lessons[i + 1]["id"]

    print(f"Parsed {len(lessons)} lesson(s) from {sys.argv[1]}\n")
    for l in lessons:
        opts = ",\n      ".join(f'"{o}"' for o in l["options"])
        print(f"""  {{
    id: "{l['id']}",
    title: "{l['title']}",
    subject: "{l['subject']}",
    subjectUrl: "subject.html",
    course: "{l['course']}",
    duration: "00:00",
    explanation: "{l['explanation']}",
    question: "{l['question']}",
    options: [
      {opts}
    ],
    correct: {l['correct']},
    prev: {f'"{l["prev"]}"' if l['prev'] else 'null'},
    next: {f'"{l["next"]}"' if l['next'] else 'null'},
    sidebar: []
  }},""")

if __name__ == "__main__":
    main()
