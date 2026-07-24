<?php
/**
 * Local preview server for Ramos Academy.
 * Serves the repo root as a static site so you can test on your phone
 * browser before committing/pushing.
 *
 * Run from the repo root:
 *   php -S 0.0.0.0:8000 tools/preview-server.php
 *
 * Then open http://localhost:8000/index.html on the same device.
 */

$root = realpath(__DIR__ . '/..');
$uri = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $root . $uri;

// Default to index.html for the root path
if ($uri === '/' || $uri === '') {
    $file = $root . '/index.html';
}

if (is_file($file)) {
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    $mime = [
        'html' => 'text/html',
        'css'  => 'text/css',
        'js'   => 'application/javascript',
        'png'  => 'image/png',
        'jpg'  => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'svg'  => 'image/svg+xml',
        'ico'  => 'image/x-icon',
    ][$ext] ?? 'text/plain';

    header("Content-Type: $mime");
    readfile($file);
} else {
    http_response_code(404);
    $notFound = $root . '/404.html';
    if (is_file($notFound)) {
        readfile($notFound);
    } else {
        echo "404 Not Found: $uri";
    }
}
