#!/usr/bin/env bash

PROJECT_DIR="/home/sstefanova/wikitech-search"
REPO_URL="https://github.com/blancadesal/wikitech-search.git"

if [ ! -d "$PROJECT_DIR" ]; then
    git clone $REPO_URL $PROJECT_DIR
fi

cd $PROJECT_DIR
git pull

# Check if .env file exists, if not generate it
# if [ ! -f "$PROJECT_DIR/.env" ]; then
#     "$PROJECT_DIR/deploy/generate-env.sh"
# fi

if [ "$(docker compose -f $PROJECT_DIR/docker-compose.yml ps -q)" ]; then
    docker compose -f $PROJECT_DIR/docker-compose.yml down -v
fi

docker compose -f $PROJECT_DIR/docker-compose.yml build
docker compose -f $PROJECT_DIR/docker-compose.yml up -d


# if [ ! -e /etc/nginx/sites-available/wikitech-search.wmcloud.org ] || \
#    ! cmp -s ./deploy/nginx.conf /etc/nginx/sites-available/wikitech-search.wmcloud.org
# then
#     sudo cp ./deploy/nginx.conf /etc/nginx/sites-available/wikitech-search.wmcloud.org

#     if [ ! -e /etc/nginx/sites-enabled/wikitech-search.wmcloud.org ]; then
#         sudo ln -s /etc/nginx/sites-available/wikitech-search.wmcloud.org /etc/nginx/sites-enabled/
#     fi

#     sudo systemctl restart nginx
# fi
