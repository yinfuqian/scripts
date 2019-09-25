<?php

$logPath = str_replace('.php', '.log', __FILE__);

error_reporting(-1);
ini_set('date.timezone', 'Asia/Shanghai');
ini_set('display_startup_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', $logPath);

//Gitlab的IP地址
//$valid_ip = array('139.196.161.0');
//Gitlab填写的令牌
$valid_token = 'fFFs.cooOOoOOOmMm';
//需要自动部署的项目目录（已写死）
$path = '/data/wwwroot/whgxwl-8008';

$client_token = isset($_SERVER['HTTP_X_GITLAB_TOKEN']) ? $_SERVER['HTTP_X_GITLAB_TOKEN'] : '';

$logFile = fopen($logPath, 'a');

$result = '[' . date('Y-m-d H:i:s', time()) . ']';

if ($client_token && $client_token == $valid_token) {
    $command = "cd {$path} 2>&1 && sudo -u www -s git pull origin  feature-net-days-hison 2>&1 || (sudo -u www -s git fetch --all 2>&1  && sudo -u www -s git reset --hard origin/feature-net-days-hison 2>&1)";
    $Res_Command = exec($command, $Arr_Debug);
    $result .= $Res_Command . "\r\n";
    foreach ($Arr_Debug as $key => $item) {
        $result .= '#' . $key . ' ' . $item . "\r\n";
    }
} else {
    $result .= 'Token mismatch!';
}

$result .= "\r\nlog\r\n";

//写入日志文件
fputs($logFile, $result);
fclose($logFile);
