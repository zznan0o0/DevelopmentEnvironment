<?php
require_once "vendor/autoload.php";

use Hprose\Client;
use Hprose\InvokeSettings;
use Hprose\ResultMode;

$client = Client::create('tcp://127.0.0.1:2016', false);
echo $client->hello("World");

echo "\n--------------------- the end --------------------------\n";