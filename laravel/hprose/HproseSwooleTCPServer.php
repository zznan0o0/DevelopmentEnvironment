<?php
require_once "vendor/autoload.php";

use Hprose\Socket\Server;

function hello($name) {
    return 'Hello ' . $name;
}

$server = new Server('tcp://0.0.0.0:2016');
$server->addFunction('hello');
echo "---------------------start tcp  port at 2016 --------------------";
$server->start();
