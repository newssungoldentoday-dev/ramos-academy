# Ramos Academy

Free, self-paced online learning platform — Khan Academy-style courses, organized by country curriculum.

Live: `https://newssungoldentoday-dev.github.io/ramos-academy`

// license

MIT — see [LICENSE](LICENSE). Will move to Archa License 1.0 once it's finalized.

---

// what it is

Ramos Academy lets anyone browse subjects, take lessons, and track progress — for free, no paywall. Core subjects (Math, Science, English, Computing) are shared globally; each country page adds subjects specific to its own curriculum (e.g. Filipino & Araling Panlipunan for the Philippines, US History & Civics for the US).

---

// stack

- Plain HTML / CSS / vanilla JS — no framework, no build step
- Single shared `style.css` across all pages
- Static site, deployable directly via GitHub Pages

---

// pages

| File | Purpose |
|---|---|
| `index.html` | Homepage |
| `countries.html` | Country picker |
| `subjects-ph.html`, `subjects-us.html`, `subjects-uk.html` | Country-specific subject lists |
| `subject.html` | Course list for a subject |
| `lesson.html` | Lesson (video + exercises + sidebar) |
| `login.html` | Log in / sign up |
| `dashboard.html` | Progress, saved courses, account |
| `search.html` | Search results |
| `about.html` | About the project |
| `contact.html` | Contact form |
| `privacy.html` | Privacy Policy |
| `terms.html` | Terms of Service |
| `404.html` | Not found page |
| `style.css` | Shared styles for all pages |

---

// design

Navy `#0F2540` + gold `#C9A86A` on cream `#FAF8F5`. Georgia serif for headings, system sans for body. No external fonts or CDNs — works offline.

---

// running locally

No build step. Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000
