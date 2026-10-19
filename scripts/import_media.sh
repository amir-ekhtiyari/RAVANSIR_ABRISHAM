#!/bin/sh
# Copy a local "media" folder (photos uploaded in the admin panel) into the running site:
#   sh scripts/import_media.sh media
set -e
cd "$(dirname "$0")/.."
SRC=${1:-media}
[ -d "$SRC" ] || { echo "Folder not found: $SRC"; exit 1; }
docker compose cp "$SRC/." web:/app/media/
# docker cp creates files as root – give them back to the app user so new uploads keep working.
docker compose exec -u root web chown -R app:app /app/media
echo "Media files imported."
