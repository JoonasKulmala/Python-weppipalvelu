# /home/joonaswsgi/public_wsgi:
# hello.py, joonas.wsgi

sudo mkdir /home/joonaswsgi/public_wsgi
sudo chown joonaswsgi:joonaswsgi /home/joonaswsgi/public_wsgi/
sudo chmod g+rwxs /home/joonaswsgi/public_wsgi/

# /etc/apache2/sites-available:
# joonaswsgi.conf

<VirtualHost *:80>
    WSGIDaemonProcess joonaswsgi user=joonaswsgi group=joonaswsgi threads=5
    WSGIScriptAlias / /home/joonaswsgi/public_wsgi/joonas.wsgi
    <Directory /home/joonaswsgi/public_wsgi/>
	WSGIScriptReloading On
	WSGIProcessGroup joonaswsgi
	WSGIApplicationGroup %{GLOBAL}
	Require all granted
    </Directory>
</VirtualHost>
