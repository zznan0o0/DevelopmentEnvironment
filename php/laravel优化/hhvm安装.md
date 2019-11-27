wget -O - http://dl.hhvm.com/conf/hhvm.gpg.key | sudo apt-key add -
echo deb http://dl.hhvm.com/ubuntu xenial main | sudo tee /etc/apt/sources.list.d/hhvm.list
apt-get update

apt-get install -y hhvm

/usr/bin/update-alternatives --install /usr/bin/php php /usr/bin/hhvm 60

service hhvm start