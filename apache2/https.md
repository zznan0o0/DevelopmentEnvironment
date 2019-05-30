

# /etc/apache2/sites-available/default-ssl.conf
    <VirtualHost _default_:443>
        ServerAdmin webmaster@localhost
                    ServerName s1.atjubo.com

        DocumentRoot /var/www/html/laravel5/public

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined


        SSLEngine on


            # 添加 SSL 协议支持协议，去掉不安全的协议
            SSLProtocol all -SSLv2 -SSLv3
            # 修改加密套件如下
            SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM
            SSLHonorCipherOrder on
            # 证书公钥配置
            SSLCertificateFile cert/wms/wms_public.crt
            # 证书私钥配置
            SSLCertificateKeyFile cert/wms/wms.key
            # 证书链配置，如果该属性开头有 '#'字符，请删除掉
            SSLCertificateChainFile cert/wms/wms_chain.crt
            

        <FilesMatch "\.(cgi|shtml|phtml|php)$">
            SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
            SSLOptions +StdEnvVars
        </Directory>



    </VirtualHost>

# 启动ssl
a2enmod ssl
service apache2 restart

# 不知道有没用
a2ensite default-ssl
service apache2 reload
