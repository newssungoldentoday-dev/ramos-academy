<?php
/**
 * Minifies a CSS or JS file by stripping comments and extra whitespace.
 * Writes a .min version alongside the original — doesn't overwrite it.
 *
 * Run:
 *   php tools/minify.php style.css
 *   php tools/minify.php lessons-url.js
 */

if ($argc < 2) {
    echo "Usage: php tools/minify.php <file.css|file.js>\n";
    exit(1);
}

$inputPath = $argv[1];
if (!file_exists($inputPath)) {
    die("File not found: $inputPath\n");
}

$content = file_get_contents($inputPath);
$ext = pathinfo($inputPath, PATHINFO_EXTENSION);

if ($ext === 'css') {
    $content = preg_replace('!/\*.*?\*/!s', '', $content);       // block comments
    $content = preg_replace('/\s+/', ' ', $content);              // collapse whitespace
    $content = preg_replace('/\s*([{}:;,])\s*/', '$1', $content); // trim around symbols
    $content = rtrim($content, '; ');
} elseif ($ext === 'js') {
    $content = preg_replace('!/\*.*?\*/!s', '', $content);        // block comments
    $content = preg_replace('/^\s*\/\/.*$/m', '', $content);      // line comments
    $content = preg_replace('/\n\s*\n/', "\n", $content);         // blank lines
    $content = preg_replace('/[ \t]+/', ' ', $content);           // collapse spaces/tabs
} else {
    die("Only .css and .js are supported.\n");
}

$outPath = preg_replace('/\.(css|js)$/', '.min.$1', $inputPath);
file_put_contents($outPath, trim($content));

$origSize = filesize($inputPath);
$newSize = filesize($outPath);
$saved = round((1 - $newSize / $origSize) * 100, 1);

echo "Minified: $outPath\n";
echo "Original: {$origSize}b → Minified: {$newSize}b ($saved% smaller)\n";
