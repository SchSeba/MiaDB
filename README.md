# MiaDB
Framework to create deployment plans on docker swarm infrastructure

## configuration
### install
run the pip install -f requirements.txt

### sercurity
change SECRET_KEY before production deployment

### storage
change <code>BasePath = "/root"</code> </br>
with the root directory storage for your containers

### docker
Download and install docker 1.12 </br>
run docker with the network parameters </br>
change the file <code>/usr/lib/systemd/system/docker.service</code>

<code> ExecStart=/usr/bin/dockerd -H 0.0.0.0:2376 -H unix:///var/run/docker.sock </code>

### database:
use django database configuration </br>
default configuration is sqlite3 </br>
can change to any database that is supported by django in the config file </br>

<code> python manage.py migrate </code>
</br>
<code> python manage.py createsuperuser </code> 

use the configuration file in the images folder

insert them into the database before deployment

### run in developer mode
<code> python manage.py runserver </code>


### run in production
for production running use gunicorn with nginx and postgres database