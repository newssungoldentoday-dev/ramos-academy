<?php
/**
 * Local test handler for the contact.html form. Saves submissions to
 * a local JSON log file — useful for testing the form flow before
 * wiring it to a real email service (GitHub Pages can't run PHP live,
 * so this only works while previewing locally via preview-server.php).
 *
 * To use: point contact.html's <form> temporarily at:
 *   action="tools/contact-handler.php" method="POST"
 * while testing locally, then swap back to a real form service (e.g.
 * Formspree) before deploying, since this script won't run on GitHub Pages.
 */

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST is allowed']);
    exit;
}

$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$message = trim($_POST['message'] ?? '');

$errors = [];
if ($name === '') $errors[] = 'Name is required';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Valid email is required';
if ($message === '') $errors[] = 'Message is required';

if ($errors) {
    http_response_code(400);
    echo json_encode(['errors' => $errors]);
    exit;
}

$logPath = __DIR__ . '/contact-submissions.json';
$submissions = file_exists($logPath) ? json_decode(file_get_contents($logPath), true) : [];

$submissions[] = [
    'name' => $name,
    'email' => $email,
    'message' => $message,
    'submitted_at' => date('c'),
];

file_put_contents($logPath, json_encode($submissions, JSON_PRETTY_PRINT));

echo json_encode(['success' => true, 'message' => 'Thanks — this was saved locally for testing.']);
