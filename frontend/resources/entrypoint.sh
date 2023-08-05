#!/bin/sh

# Generate environment variables
cd /usr/share/nginx
envsubst < docker.blueprint.env > docker.env

# Add environment variables to index html file
CONFIGURATION="window.__env__ = $(cat /usr/share/nginx/docker.env | tr -d '\n');"
sed -i "s@// CONFIGURATION PLACEHOLDER@${CONFIGURATION}@" /usr/share/nginx/html/index.html

exec "$@"