#!/usr/bin/env bash

mkdir -p ./data/postgres

docker run -it --rm --name mypostgres -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password \
    -v "$PWD/.data/postgres":/var/lib/postgresql/data -p 5432:5432 postgres:13.0