<?php
$dsn = 'sqlsrv:server=192.168.8.44;Database=WebPlatform';
$user = 'jackle';
$password = 'Jackle844';

$conn = new PDO($dsn, $user, $password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

function JSON($data, $code = 200) {
    http_response_code($code);
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data,JSON_UNESCAPED_UNICODE);
    die();
}
?>
