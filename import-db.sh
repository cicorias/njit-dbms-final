#!/usr/bin/env bash

cd ./hotelapp

python ./manage.py migrate

DBFILE=$(pwd)/db.sqlite3

echo "using $DBFILE"

for f in ../data/*.sql;
do 
  sqlite3 $DBFILE ".read $f"
done