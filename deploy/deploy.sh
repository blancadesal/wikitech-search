#!/usr/bin/env bash

cd /home/sstefanova/wikitech-search
git pull

cp ./nginx.conf /etc/nginx/sites-available/wikitech-search.wmcloud.org

sudo ln -s /etc/nginx/sites-available/wikitech-search.wmcloud.org /etc/nginx/sites-enabled/

sudo systemctl restart nginx

docker-compose down -v
docker-compose build
docker-compose up -d
