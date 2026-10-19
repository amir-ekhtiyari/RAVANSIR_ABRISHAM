#!/bin/sh
# Backup database + uploaded files into ./backups (keeps the last 14). Run from the project folder:
#   sh scripts/backup.sh          (add to cron:  0 3 * * * cd /opt/ravansir && sh scripts/backup.sh)
set -e
cd "$(dirname "$0")/.."
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p backups
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --format=custom' > "backups/db-$STAMP.dump"
docker compose exec -T web tar czf - -C /app media > "backups/media-$STAMP.tgz"
ls -1t backups/db-*.dump | tail -n +15 | xargs -r rm --
ls -1t backups/media-*.tgz | tail -n +15 | xargs -r rm --
echo "Backup saved: backups/db-$STAMP.dump, backups/media-$STAMP.tgz"
