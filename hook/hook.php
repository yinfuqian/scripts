<?php
//获取http 头
$logPath = str_replace('.php', '.log', __FILE__);

error_reporting(-1);
ini_set('date.timezone', 'Asia/Shanghai');
ini_set('display_startup_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', $logPath);

$secret = 'fFFs.cooOOoOOOmMm'; #在GitHub上填写的secret
$headers = array();
//Apache服务器才支持getallheaders函数
if (!function_exists('getallheaders')) {
    foreach ($_SERVER as $name => $value) {
        if (substr($name, 0, 5) == 'HTTP_') {
            $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value;
        }
    }
}else
{
    $headers = getallheaders();
}
//github发送过来的签名
$hubSignature = $headers['X-Hub-Signature'];
list($algo, $hash) = explode('=', $hubSignature, 2);

// 获取body内容
$payload = file_get_contents('php://input');


$logFile = fopen($logPath, 'a');
$result = '[' . date('Y-m-d H:i:s', time()) . ']';

// 计算签名
$payloadHash = hash_hmac($algo, $payload, $secret);
$target = "/var/www/html";
// 判断签名是否匹配
if ($hash === $payloadHash) {
           //调用shell
   //echo shell_exec("bash /var/www/html/hook/git.sh");
   $command = "bash /var/www/html/hook/git.sh";
   $Res_Command = exec($command, $Arr_Debug);
   $result .= $Res_Command . "\r\n";
   foreach ($Arr_Debug as $key => $item) {
        $result .= '#' . $key . ' ' . $item . "\r\n";
    }  
}else{
   $result .= 'Token mismatch!';
}

$result .= "\r\nlog\r\n";

//写入日志文件
fputs($logFile, $result);
fclose($logFile);

