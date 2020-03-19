groupadd docker
gpasswd -a dever docker
systemctl restart docker
docker ps