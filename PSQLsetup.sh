#!/bin/bash

# Set of commands to get react running in a new folder (some commands are folder specific)
sudo yum update
sudo /usr/local/bin/pip install --upgrade pip
sudo /usr/local/bin/pip install psycopg2-binary
sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1
sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
sudo service postgresql initdb
sudo service postgresql start
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
