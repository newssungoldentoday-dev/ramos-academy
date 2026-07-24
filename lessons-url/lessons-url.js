// Central registry of every lesson URL + metadata.
// Add a new object here whenever you add a new lessons/*.html file.
// Used by search.html to render results dynamically instead of hardcoded HTML.

const LESSONS = [
  {
    id: "math-arithmetic-fractions",
    title: "Fractions",
    url: "lessons/math-arithmetic-fractions.html",
    subject: "Mathematics",
    course: "Arithmetic",
    country: "core",
    duration: "08:15"
  },
  {
    id: "math-algebra1-linear-equations",
    title: "Solving Linear Equations",
    url: "lessons/math-algebra1-linear-equations.html",
    subject: "Mathematics",
    course: "Algebra I",
    country: "core",
    duration: "12:34"
  },
  {
    id: "math-algebra1-inequalities",
    title: "Inequalities",
    url: "lessons/math-algebra1-inequalities.html",
    subject: "Mathematics",
    course: "Algebra I",
    country: "core",
    duration: "09:10"
  },
  {
    id: "math-algebra1-graphing-lines",
    title: "Graphing Linear Equations",
    url: "lessons/math-algebra1-graphing-lines.html",
    subject: "Mathematics",
    course: "Algebra I",
    country: "core",
    duration: "09:52"
  },
  {
    id: "math-algebra1-systems",
    title: "Systems of Linear Equations",
    url: "lessons/math-algebra1-systems.html",
    subject: "Mathematics",
    course: "Algebra I",
    country: "core",
    duration: "11:47"
  }
];

// Simple text search across title, subject, course
function searchLessons(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return LESSONS.filter(l =>
    l.title.toLowerCase().includes(q) ||
    l.subject.toLowerCase().includes(q) ||
    l.course.toLowerCase().includes(q)
  );
    }
