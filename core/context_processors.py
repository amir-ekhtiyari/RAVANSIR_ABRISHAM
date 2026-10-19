import json

from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url
from django.utils.translation import gettext_lazy as _

from .models import CompanyInfo, current_lang

NAV = [
    ('home', _('Home'), 'pages:home'),
    ('services', _('Services'), 'services:list'),
    ('routes', _('Routes'), 'pages:routes'),
    ('about', _('About Us'), 'pages:about'),
    ('contact', _('Contact'), 'contact:page'),
]


# (code, short label shown in the switcher, full name for screen readers – each in its own language)
LANG_LABELS = [('fa', 'فارسی', 'فارسی'), ('en', 'EN', 'English'), ('tr', 'TR', 'Türkçe')]


def _cached_list(key, app_label, model_name):
    from django.apps import apps
    from django.core.cache import cache
    items = cache.get(key)
    if items is None:
        items = list(apps.get_model(app_label, model_name).objects.published())
        cache.set(key, items, 300)
    return items


def organization_jsonld(company):
    """schema.org data built only from the stored company facts (nothing invented)."""
    if company is None:
        return ''
    data = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': company.tr('name'),
        'alternateName': [n for n in (company.name_fa, company.name_en, company.name_tr) if n],
        'url': settings.SITE_URL + '/',
        'logo': settings.SITE_URL + static('images/rsa-mark.png'),
        'email': company.email,
        'telephone': company.office_phone_tel,
        'description': company.tr('short_description'),
        'contactPoint': [
            {'@type': 'ContactPoint', 'telephone': company.office_phone_tel, 'contactType': 'customer service',
             'availableLanguage': ['fa', 'en', 'tr']},
            {'@type': 'ContactPoint', 'telephone': company.mobile_tel, 'contactType': 'sales'},
        ],
        'areaServed': ['IR', 'TR', 'IQ', 'AZ', 'Europe'],
    }
    if company.work_phone:
        data['contactPoint'].append({'@type': 'ContactPoint', 'telephone': company.work_phone_tel,
                                     'contactType': 'customer service'})
    if company.tr('address'):
        data['address'] = {'@type': 'PostalAddress', 'streetAddress': company.tr('address'),
                           'addressLocality': 'Tehran', 'addressCountry': 'IR'}
    if company.tr('branch_address'):
        branch = {'@type': 'Place', 'name': 'Marand',
                  'address': {'@type': 'PostalAddress', 'streetAddress': company.tr('branch_address'),
                              'addressLocality': 'Marand', 'addressCountry': 'IR'}}
        if company.branch_phone:
            branch['telephone'] = company.branch_phone_tel
        data['location'] = [branch]
    # Escape "<" so the JSON can never close the <script> element.
    return json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')


def asset_version():
    """Cache-buster for site.css/site.js in development (production uses hashed file names)."""
    if not settings.DEBUG:
        return ''
    stamps = []
    for name in ('css/site.css', 'js/site.js'):
        for folder in settings.STATICFILES_DIRS:
            try:
                stamps.append(int((folder / name).stat().st_mtime))
            except OSError:
                pass
    return str(max(stamps)) if stamps else ''


def site(request):
    lang = current_lang()
    path = request.get_full_path()
    company = CompanyInfo.load()
    return {
        'company': company,
        'company_jsonld': organization_jsonld(company),
        'lang': lang,
        'dir': 'rtl' if lang == 'fa' else 'ltr',
        'nav_items': NAV,
        'lang_switch': [
            {'code': code, 'label': label, 'title': title, 'url': translate_url(path, code), 'active': lang == code}
            for code, label, title in LANG_LABELS
        ],
        'admin_url': '/' + settings.ADMIN_URL,
        'asset_version': asset_version(),
        'footer_services': _cached_list('core:footer:services', 'services', 'Service'),
        'footer_routes': _cached_list('core:footer:routes', 'services', 'Route'),
    }
