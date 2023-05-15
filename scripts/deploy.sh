#!/usr/bin/env bash

cd /home/sstefanova/wikitech-search
git pull
docker-compose down -v
docker-compose build
docker-compose up -d
