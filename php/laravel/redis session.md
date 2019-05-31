sudo apt-get install redis-server -y

composer 安装 redis:

composer require predis/predis

配置 redis 连接（config/database.php 配置文件）
打开 database.php 文件，可以看到，其实 database.php 里已经有一个 redis 的配置，redis 配置项里有一个 default 配置数组
你可以理解成那是 redis 缓存的默认配置，redis 的默认读写操作就通过这个配置来连接 redis，这里我们添加一个新配置来区分做 session 的保存（当然，你要直接使用 default 配置也是可以的）
添加 session 连接配置如下：


'redis' => [

    'cluster' => false,

    'default' => [
        'host'     => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD', null),
        'port'     => env('REDIS_PORT', 6379),
        'database' => 0,
    ],
    
    'session' => [
        'host'     => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD', null),
        'port'     => env('REDIS_PORT', 6379),
        'database' => 1,
    ],
],

关键是配置的配置是 'database' => 1，redis 有一个数据库概念，默认支持最多 16 个数据库，这里 session 配置使用了 1 号数据库
配置 sesison 驱动（config/session.php 配置文件）
首先，session 驱动方式改 redis:

'driver' => env('SESSION_DRIVER', 'redis'),

然后，告诉它你要使用哪个 redis 连接配置（这里我们使用 session 配置，当然，就如上所说，你要配置成 default 配置也是可以的）:

'connection' => 'session',

修改 .env 文件进行测试:

SESSION_DRIVER=redis

