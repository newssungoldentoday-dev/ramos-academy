<?php
/**
 * Scans the repo root for .html files and generates sitemap.xml
 * for search engines. Run before pushing a new batch of pages.
 *
 * Run:
 *   php tools/sitemap-generator.php
 */

$root = realpath(__DIR__ . '/..');
$baseUrl = 'https://newssungoldentoday-dev.github.io/ramos-academy';

// Folders to skip entirely
$skipDirs = ['tools', '.git', 'node_modules'];

function scanHtmlFiles($dir, $root, $skipDirs) {
    $files = [];
    $items = scandir($dir);

    foreach ($items as $item) {
        if ($item === '.' || $item === '..') continue;

        $path = $dir . '/' . $item;
        $relative = ltrim(str_replace($root, '', $path), '/');

        if (is_dir($path)) {
            $topLevel = explode('/', $relative)[0];
            if (in_array($topLevel, $skipDirs)) continue;
            $files = array_merge($files, scanHtmlFiles($path, $root, $skipDirs));
        } elseif (pathinfo($item, PATHINFO_EXTENSION) === 'html') {
            $files[] = $relative;
        }
    }

    return $files;
}

$htmlFiles = scanHtmlFiles($root, $root, $skipDirs);
sort($htmlFiles);

echo "Found " . count($htmlFiles) . " HTML file(s):\n";
foreach ($htmlFiles as $f) {
    echo "  - $f\n";
}

$xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>');

foreach ($htmlFiles as $file) {
    // Skip the lesson template placeholder and 404
    if (basename($file) === '404.html') continue;

    $url = $xml->addChild('url');
    $loc = $file === 'index.html' ? $baseUrl . '/' : $baseUrl . '/' . $file;
    $url->addChild('loc', htmlspecialchars($loc));
    $url->addChild('lastmod', date('Y-m-d'));
    $url->addChild('changefreq', 'monthly');
    $url->addChild('priority', $file === 'index.html' ? '1.0' : '0.7');
}

$dom = new DOMDocument('1.0');
$dom->preserveWhiteSpace = false;
$dom->formatOutput = true;
$dom->loadXML($xml->asXML());
$outPath = $root . '/sitemap.xml';
$dom->save($outPath);

echo "\nsitemap.xml written to $outPath\n";
echo "Remember to commit and push it.\n";
