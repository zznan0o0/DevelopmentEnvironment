1. 添加远程用户
> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'youpassword' WITH GRANT OPTION;
2. 刷新用户
> FLUSH PRIVILEGES;
3. 注释bind-address
> vim /etc/mysql/mysql.conf.d/mysqld.cnf
> #bind-address           = 127.0.0.1
4. 跳过dns检查
> vim /etc/mysql/mysql.conf.d/mysqld.cnf
> [mysqld] 下添加
> skip-name-resolve
