#!/usr/bin/env bash

cd /home/sstefanova/wikitech-search
git pull


if [ "$(docker compose ps -q)" ]; then
    docker compose down -v
fi

docker compose build
docker compose up -d


if [ ! -e /etc/nginx/sites-available/wikitech-search.wmcloud.org ] || \
   ! cmp -s ./deploy/nginx.conf /etc/nginx/sites-available/wikitech-search.wmcloud.org
then
    sudo cp ./deploy/nginx.conf /etc/nginx/sites-available/wikitech-search.wmcloud.org

    if [ ! -e /etc/nginx/sites-enabled/wikitech-search.wmcloud.org ]; then
        sudo ln -s /etc/nginx/sites-available/wikitech-search.wmcloud.org /etc/nginx/sites-enabled/
    fi

    sudo systemctl restart nginx
fi
