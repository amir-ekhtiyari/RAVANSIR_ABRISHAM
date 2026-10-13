"""
Real photographs used across the site live in static/images/photos/<key>.webp (or .jpg/.png).

Keys (put a file with that name in the folder and it appears on the site automatically):
    hero, about, routes, why, cta, contact, page,
    fleet-curtain, fleet-tanker, fleet-reefer, fleet-transit,
    svc-<service slug>   e.g. svc-international-transit

Every lookup takes a chain of keys and uses the first file that exists, so a handful of good photos
can cover the whole site. Photos uploaded in the admin panel (hero, about, fleet) take precedence.
"""

from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.templatetags.static import static

PHOTO_DIR = Path(settings.BASE_DIR) / 'static' / 'images' / 'photos'
EXTENSIONS = ('webp', 'jpg', 'jpeg', 'png')
# When nothing more specific exists, fall back to these general road/truck photos in order.
GENERAL = ('road', 'hero', 'about', 'why', 'routes', 'cta')


def _existing(key):
    for ext in EXTENSIONS:
        if (PHOTO_DIR / f'{key}.{ext}').is_file():
            return f'images/photos/{key}.{ext}'
    return None


@lru_cache(maxsize=256)
def _cached(keys):
    for key in keys:
        found = _existing(key)
        if found:
            return static(found)
    return ''


def photo_url(*keys, general=True):
    chain = tuple(keys) + (GENERAL if general else ())
    if settings.DEBUG:            # pick up newly added files without a restart while developing
        _cached.cache_clear()
    return _cached(chain)
