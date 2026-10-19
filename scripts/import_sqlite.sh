#!/bin/sh
# Copy the content of a local db.sqlite3 (company info, services, routes, fleet, admin user, requests)
# into the PostgreSQL database of the running stack:  sh scripts/import_sqlite.sh db.sqlite3
set -e
cd "$(dirname "$0")/.."
SRC=${1:-db.sqlite3}
[ -f "$SRC" ] || { echo "File not found: $SRC"; exit 1; }
docker compose cp "$SRC" web:/tmp/import.sqlite3
docker compose exec web python manage.py setup_postgres --sqlite /tmp/import.sqlite3
docker compose exec web rm -f /tmp/import.sqlite3
