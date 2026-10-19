"""Docker HEALTHCHECK: GET /healthz on the local gunicorn using an allowed Host header."""
import os
import sys
import urllib.request

host = (os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')[0].strip() or 'localhost').lstrip('.')
request = urllib.request.Request(f"http://127.0.0.1:{os.environ.get('PORT', '8000')}/healthz",
                                 headers={'Host': host, 'X-Forwarded-Proto': 'https'})
try:
    with urllib.request.urlopen(request, timeout=4) as response:
        sys.exit(0 if response.status == 200 else 1)
except Exception as exc:  # noqa: BLE001
    print(exc, file=sys.stderr)
    sys.exit(1)
