#!/bin/sh
# Prepares the container, then runs the command (gunicorn by default).
set -e

if [ -z "$DJANGO_SECRET_KEY" ] || [ "$DJANGO_SECRET_KEY" = "change-me" ]; then
  echo "ERROR: set DJANGO_SECRET_KEY in .env" >&2
  exit 1
fi

if [ -n "$POSTGRES_DB" ]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432} ..."
  python - <<'PY'
import os, sys, time
import psycopg
for attempt in range(60):
    try:
        psycopg.connect(host=os.environ.get('POSTGRES_HOST', 'db'), port=os.environ.get('POSTGRES_PORT', '5432'),
                        user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'),
                        dbname=os.environ['POSTGRES_DB'], connect_timeout=3).close()
        print('PostgreSQL is ready.')
        sys.exit(0)
    except psycopg.OperationalError as exc:
        last = exc
        time.sleep(2)
print(f'PostgreSQL did not become ready: {last}', file=sys.stderr)
sys.exit(1)
PY
fi

if [ "${DJANGO_MIGRATE:-1}" = "1" ]; then
  python manage.py migrate --noinput
fi

# Static files go to a volume shared with the web server (Caddy) and use hashed names.
python manage.py collectstatic --noinput --clear -v 0
echo "Static files collected."

exec "$@"
