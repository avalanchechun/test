這是我的程式碼，我想撰寫一個功能是紀錄進來這個網頁的人的IP, USER名稱, 進入該網頁的名稱,CLICK_TIME接著寫入資料表當中[WebPlatForm].[dbo].[WebPlatForm_Counter]，我有個php程式是有這樣的功能如下:<?php

    include_once "db_config_844.php";

    if (isset($_GET['user'])) {
        $user = $_GET['user'];
    } else {
        $user = '';
    }

    $user .= "(" . gethostbyaddr($_SERVER['REMOTE_ADDR']) . ")";

    if (!empty($_SERVER["HTTP_CLIENT_IP"])){
        $ip = $_SERVER["HTTP_CLIENT_IP"];
    }elseif(!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
        $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
    }else{
        $ip = $_SERVER["REMOTE_ADDR"];
    }

    $clicks_link = "RDMPLOG-CtrlToWafer";
    $clicks_user = $user;
    $statement = $conn->prepare("insert into WebPlatForm_Counter([IP],[USER],[REPORT],[CLICK_TIME]) VALUES('$ip','$clicks_user','$clicks_link',convert(varchar(50),getdate(),20))");
    $result = $statement->execute();
?>
請幫我整合到原來的jsp程式碼當中
