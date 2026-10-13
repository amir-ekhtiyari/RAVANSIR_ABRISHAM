from django import template
from django.utils.html import format_html

from core.models import current_lang

register = template.Library()

FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


@register.filter
def local_digits(value):
    """Persian digits on the Persian site, Latin digits on the English site."""
    text = '' if value is None else str(value)
    return text.translate(FA_DIGITS) if current_lang() == 'fa' else text


@register.filter
def tr(obj, field):
    """{{ service|tr:'title' }} → the active language's text."""
    return obj.tr(field) if obj is not None else ''


@register.filter
def tr_lines(obj, field):
    return obj.tr_lines(field) if obj is not None else []


@register.simple_tag
def icon(name, size=20, cls=''):
    """Inline reference to the Lucide sprite (static/icons/sprite.svg is inlined in base.html)."""
    return format_html(
        '<svg class="icon {}" width="{}" height="{}" aria-hidden="true" focusable="false"><use href="#i-{}"></use></svg>',
        cls, size, size, name,
    )


@register.simple_tag
def phone_display(number):
    """0218893 5889 → 021 8893 5889 / 0914 491 8300 (grouped, localised digits)."""
    digits = ''.join(ch for ch in str(number) if ch.isdigit())
    if digits.startswith('09') and len(digits) == 11:
        grouped = f'{digits[:4]} {digits[4:7]} {digits[7:]}'
    elif digits.startswith('0') and len(digits) == 11:
        grouped = f'{digits[:3]} {digits[3:7]} {digits[7:]}'
    else:
        grouped = digits
    return local_digits(grouped)


def _jalali_year(date):
    """Gregorian → Jalali year (enough for a copyright line; the year turns at Nowruz ≈ 21 March)."""
    year = date.year - 621
    if (date.month, date.day) < (3, 21):
        year -= 1
    return year


@register.simple_tag
def copyright_year():
    from django.utils import timezone
    today = timezone.localdate()
    return local_digits(_jalali_year(today) if current_lang() == 'fa' else today.year)


@register.filter
def first_sentences(text, count=1):
    """The first `count` sentences of a text (Persian or English full stops)."""
    import re
    parts = re.split(r'(?<=[.!؟?])\s+', (text or '').strip())
    return ' '.join(parts[:int(count)])


@register.simple_tag
def photo(*keys, general=True):
    """{% photo 'fleet-tanker' 'svc-international-road-transportation' as url %} → static URL or ''."""
    from core.photos import photo_url
    return photo_url(*keys, general=general)
