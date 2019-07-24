1. 安装OpenSSH server
> apt-get install openssh-server
2. 编辑sshd_config
> vim /etc/ssh/sshd_config
> PermitRootLogin no 改为 yes
> PasswordAuthentication no 改为 yes