Ubuntu 16.4系统下安装docker


一、docker安装
1，卸载旧版本docker
全新安装时，无需执行该步骤

$ sudo apt-get remove docker docker-engine docker.io
2，更新系统软件
$ sudo apt-get update
3，安装依赖包
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
4，添加官方密钥
执行该命令时，如遇到长时间没有响应说明网络连接不到docker网站，需要使用代-理进行。

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
显示OK,表示添加成功.

5，添加仓库
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
6，再次更新软件
经实践，这一步不能够省略，我们需要再次把软件更新到最新，否则下一步有可能会报错。

$ sudo apt-get update
7，安装docker
如果想指定安装某一版本，可使用 sudo apt-get install docker-ce=<VERSION>  命令，把<VERSION>替换为具体版本即可。

* 如果下不动使用阿里云 apt仓库

如果你已经添加过官网的源 请在/etc/apt/sources.list 最后那几行删掉（有一个是那刚才添加的国外deb源 不然你每次apt update 都会爆一个蛋疼的错Failed to fetch https://apt.dockerproject.org/repo/dists/ubun），然后执行下面的阿里云安装源



$ curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

$ sudo add-apt-repository \
     "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
     $(lsb_release -cs) \
     stable"

以下命令没有指定版本，默认就会安装最新版

$ sudo apt-get install docker-ce
8，查看docker版本
$ docker -v
显示“Docker version 17.09.0-ce, build afdb6d4”字样，表示安装成功。

二、docker-compose安装
1，下载docker-compose
$ sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
2，授权
$ sudo chmod +x /usr/local/bin/docker-compose
3，查看版本信息
$ docker-compose --version
显示出版本信息，即安装成功。

三、docker-machine安装
说明：docker-machine的使用是要基于virtualBox的。如果没有安装安装过，请先安装virtualBox。

1，安装virtualBox
登录virtualBox官网：https://www.virtualbox.org/wiki/Linux_Downloads

找到"Ubuntu 16.04 ("Xenial")  i386 |  AMD64"字样，点击“AMD64”进行下载。

下载后，执行以下命令进行安装：

$ sudo dpkg -i virtualbox-5.2_5.2.0-118431_Ubuntu_xenial_amd64.deb
2，下载并安装docker-machine
$ curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
3，查看版本信息
$ docker-machine version
显示出版本信息，即安装成功。