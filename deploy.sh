#!/bin/bash
echo '#########################################################'
now=$( date )
echo Script started at $now
source ~/.bashrc
conda activate coil_clean_project_v2
docker pull mysql/mysql-server:8.0
docker run  --name=CoilCleanDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -d mysql/mysql-server:8.0
python3 create_db.py

flask run
