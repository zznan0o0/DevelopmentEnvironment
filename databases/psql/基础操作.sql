基础操作：
接入PostgreSQL数据库: psql -h IP地址 -p 端口 -U 数据库名

1、列举数据库：\l
2、选择数据库：\c 数据库名
3、查看该某个库中的所有表：\dt
4、切换数据库：\c interface
5、查看某个库中的某个表结构：\d 表名
6、查看某个库中某个表的记录：select * from apps limit 1;
7、显示字符集：\encoding
8、退出psgl：\q


创建库表：
1.创建数据库 
> create database xxxx;

2.创建表

create database db_human_eft_aly;

\c db_human_eft_aly;

DROP TABLE IF EXISTS "public"."tb_goods_collocation";
CREATE TABLE "public"."tb_goods_collocation" (
  "id" serial NOT NULL,
  sale_price decimal(16,4) not null DEFAULT 0,
  sale_ton decimal(16,4) not null DEFAULT 0,
  count integer not null DEFAULT 0,
  goods json not null DEFAULT '[]',
  state varchar(50) not null DEFAULT '',
  remark varchar(255) not null DEFAULT '',
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN "public"."tb_goods_collocation"."id" IS 'id';
COMMENT ON COLUMN "public"."tb_goods_collocation"."sale_price" IS '总销售额';
COMMENT ON COLUMN "public"."tb_goods_collocation"."sale_ton" IS '总销售量';
COMMENT ON COLUMN "public"."tb_goods_collocation"."goods" IS '商品合集';
COMMENT ON COLUMN "public"."tb_goods_collocation"."state" IS '状态';
COMMENT ON COLUMN "public"."tb_goods_collocation"."remark" IS '备注';
COMMENT ON COLUMN "public"."tb_goods_collocation"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."tb_goods_collocation"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."tb_goods_collocation"."count" IS '出现次数';


ALTER TABLE "public"."tb_goods_collocation" ADD CONSTRAINT "tb_goods_collocation_pkey" PRIMARY KEY ("id");


用户：
1.修改密码
 ALTER USER postgres WITH PASSWORD 'postgres';


远程链接：

配置文件在/etc/postgresql/x/main下
1. postgresql.conf 添加 listen_addresses = '*'
2. pg_hba.conf 添加 host  all  all 0.0.0.0/0 md5
3. 重启 service postgresql restart
4. 防火墙端口 iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 5432 -j ACCEPT


备份:

pg_dump 数据库名 -h 127.0.0.1 -p 5432 -U postgres > 导出文件名

恢复:
create database 数据库名;
psql 数据库名 < 导入文件名

php:
apt install php7.1-pgsql


'db_human_eft_aly' => [
    'driver' => 'pgsql',
    'host' => '127.0.0.1',
    'port' => '5432',
    'database' => 'db_human_eft_aly',
    'username' => 'postgres',
    'password' =>'postgres',
    'charset' => 'utf8',
    'prefix' => '',
    'schema' => 'public',
    'sslmode' => 'prefer',
],
