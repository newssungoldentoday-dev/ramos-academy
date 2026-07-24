<?php
/**
 * Renders every lesson from lessons-url.js as a browsable local page,
 * so you can review your full lesson catalog without opening each one.
 *
 * Run:
 *   php -S 0.0.0.0:8001 tools/lessons-viewer.php
 * Then open http://localhost:8001/tools/lessons-viewer.php
 */

$root = realpath(__DIR__ . '/..');
$jsPath = $root . '/lessons-url.js';

if (!file_exists($jsPath)) {
    die('lessons-url.js not found at ' . $jsPath);
}

$js = file_get_contents($jsPath);

// Extract the LESSONS array block
preg_match('/const LESSONS\s*=\s*(\[.*?\]);/s', $js, $m);
if (!$m) {
    die('Could not find LESSONS array in lessons-url.js');
}

$raw = $m[1];
// Loosely convert JS object literal syntax to JSON
$raw = preg_replace('/(\w+)\s*:/', '"$1":', $raw);
$raw = preg_replace('/,(\s*[\]}])/', '$1', $raw); // trailing commas
$lessons = json_decode($raw, true);

if ($lessons === null) {
    die('Could not parse LESSONS as JSON. Check lessons-url.js formatting.');
}

// Group by subject > course
$grouped = [];
foreach ($lessons as $l) {
    $grouped[$l['subject']][$l['course']][] = $l;
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Lessons Viewer (local)</title>
<style>
  body{font-family:sans-serif;max-width:800px;margin:30px auto;padding:0 16px;color:#0F2540}
  h1{border-bottom:2px solid #C9A86A;padding-bottom:8px}
  h2{margin-top:28px;color:#C9A86A}
  h3{margin-top:16px;font-size:15px}
  .lesson{border:1px solid #eee;border-radius:8px;padding:10px 14px;margin-top:8px}
  .lesson a{color:#0F2540;font-weight:600;text-decoration:none}
  .meta{font-size:12px;color:#888;margin-top:4px}
  .count{font-size:13px;color:#888}
</style>
</head>
<body>
<h1>Lessons Viewer <span class="count">(<?= count($lessons) ?> total)</span></h1>

<?php foreach ($grouped as $subject => $courses): ?>
  <h2><?= htmlspecialchars($subject) ?></h2>
  <?php foreach ($courses as $course => $items): ?>
    <h3><?= htmlspecialchars($course) ?> (<?= count($items) ?>)</h3>
    <?php foreach ($items as $l): ?>
      <div class="lesson">
        <a href="/lessons/lessons.html?id=<?= urlencode($l['id']) ?>" target="_blank">
          <?= htmlspecialchars($l['title']) ?>
        </a>
        <div class="meta">
          id: <?= htmlspecialchars($l['id']) ?> ·
          duration: <?= htmlspecialchars($l['duration'] ?? '00:00') ?> ·
          prev: <?= htmlspecialchars($l['prev'] ?? 'none') ?> ·
          next: <?= htmlspecialchars($l['next'] ?? 'none') ?>
        </div>
      </div>
    <?php endforeach; ?>
  <?php endforeach; ?>
<?php endforeach; ?>

</body>
</html>
