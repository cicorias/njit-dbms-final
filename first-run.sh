#!/usr/bin/env bash
set -euxo pipefail


cd ./hotelapp
python ./manage.py migrate

echo "from users.models import CustomUser; CustomUser.objects.create_superuser('root@example.com', 'password')" | python ./manage.py shell

DBFILE=$(pwd)/db.sqlite3

echo "using $DBFILE"

for f in ../data/*.sql;
do 
  #sqlite3 $DBFILE ".read $f"
  python ./manage.py dbshell ".read $f"
done

echo "at this point you should be able to runserver and see some seed data."