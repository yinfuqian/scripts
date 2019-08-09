
<?php   
$secret = 'AaBbCcDdEe123{}'; #在GitHub上填写的secret
//获取http 头
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

// 计算签名
$payloadHash = hash_hmac($algo, $payload, $secret);
$target = "/home/wwwroot/cxzfbAdmin";
// 判断签名是否匹配
if ($hash === $payloadHash) {
           //调用shell
    echo shell_exec("./git.sh");
}else{
    http_response_code(404);//返回404，反正都执行了返回404也无所谓
}

