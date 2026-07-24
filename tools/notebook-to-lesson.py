#!/usr/bin/env python3
"""
Converts physical notebook lesson content into a ready-to-paste
JS object for lessons-url.js. Run in Termux:

    python3 tools/notebook-to-lesson.py
"""

def ask(prompt, required=True):
    while True:
        val = input(prompt).strip()
        if val or not required:
            return val
        print("  (required, try again)")

def slugify(text):
    return text.lower().strip().replace(" ", "-").replace("'", "")

def main():
    print("=== Notebook → Lesson Converter ===\n")

    title = ask("Lesson title: ")
    slug = slugify(ask(f"URL slug [{slugify(title)}]: ", required=False) or title)
    subject = ask("Subject (e.g. Mathematics, Science): ")
    course = ask("Course (e.g. Algebra I, Biology): ")
    duration = ask("Video duration [00:00]: ", required=False) or "00:00"
    explanation = ask("Explanation/notes: ")
    question = ask("Practice question: ")

    options = []
    print("Enter answer options (blank line to stop):")
    while True:
        opt = input(f"  Option {len(options)+1}: ").strip()
        if not opt:
            break
        options.append(opt)

    correct = int(ask(f"Index of correct answer (0-{len(options)-1}): "))
    prev_id = ask("Previous lesson id [none]: ", required=False) or "null"
    next_id = ask("Next lesson id [none]: ", required=False) or "null"

    prev_val = f'"{prev_id}"' if prev_id != "null" else "null"
    next_val = f'"{next_id}"' if next_id != "null" else "null"

    opts_js = ",\n      ".join(f'"{o}"' for o in options)

    js = f"""  {{
    id: "{slug}",
    title: "{title}",
    subject: "{subject}",
    subjectUrl: "subject.html",
    course: "{course}",
    duration: "{duration}",
    explanation: "{explanation}",
    question: "{question}",
    options: [
      {opts_js}
    ],
    correct: {correct},
    prev: {prev_val},
    next: {next_val},
    sidebar: [
      {{ id: "{slug}", title: "{title}", duration: "{duration}" }}
    ]
  }}"""

    print("\n=== Paste this into the LESSONS array in lessons-url.js ===\n")
    print(js)
    print(f"\nLive URL will be:\nlessons/lessons.html?id={slug}\n")

if __name__ == "__main__":
    main()
