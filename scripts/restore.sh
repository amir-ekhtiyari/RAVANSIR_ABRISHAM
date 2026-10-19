#!/bin/sh
# Restore a database backup:  sh scripts/restore.sh backups/db-YYYYMMDD-HHMMSS.dump
set -e
cd "$(dirname "$0")/.."
[ -f "$1" ] || { echo "usage: sh scripts/restore.sh backups/db-....dump"; exit 1; }
docker compose exec -T db sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists --no-owner' < "$1"
docker compose restart web
echo "Restored $1"
