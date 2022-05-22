# biblio-crawl

## Installation WSGI


Créer un répertoire et y cloner le projet
```bash
mkdir /var/www/FLASK/bibli/
cd /var/www/FLASK/bibli/
git clone https://github.com/Gaspi/biblio-crawl.git bibli
```

Créer un dossier de logs
```bash
mkdir /var/www/FLASK/bibli/logs
```

Créer un fichier `bibli.wsgi` contenant le code suivant
```python
import sys
sys.path.insert(0, '/var/www/FLASK/bibli/')
sys.path.insert(0, '/var/www/FLASK/bibli/bibli/')
from bibli import app as application
```


Créer une configuration Apache2 `/etc/apache2/sites-available/bibli.conf` avec le code suivant
```
<VirtualHost *:8080>
    WSGIDaemonProcess bibli user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/FLASK/bibli/bibli.wsgi

    Alias "/static/" "/var/www/FLASK/bibli/bibli/static/"
    <Directory "/var/www/FLASK/bibli/bibli/static/">
        Order allow,deny
        Allow from all
    </Directory>

    <Directory /var/www/FLASK/bibli/>
        WSGIProcessGroup bibli
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

    ErrorLog /var/www/FLASK/bibli/logs/error.log
    CustomLog /var/www/FLASK/bibli/logs/access.log combined
</VirtualHost>
```

