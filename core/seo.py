"""Page titles, descriptions and alternate-language links for every page (one place to edit)."""

from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url
from django.utils.translation import gettext as _

from .models import CompanyInfo, current_lang


def _texts():
    return {
        'home': (
            _('International Road Freight & Transit | Iran – Turkey – Europe'),
            _('International road transportation, transit and freight forwarding between Iran, Turkey, '
              'Europe and the region. Customs coordination at Bazargan, Razi, Serow and Jolfa. '
              'Request a transport consultation.'),
        ),
        'services': (
            _('Services – Road Freight, Transit, Forwarding & Customs Consulting'),
            _('International road transportation, transit through Iranian borders, freight forwarding, export '
              'transportation and transport and customs consulting.'),
        ),
        'routes': (
            _('Active Routes – Iran, Turkey, Europe, Iraq and Azerbaijan'),
            _('Our active international road freight routes: Turkey to Iran, Iran to Turkey, Iran to Europe, '
              'Iran to Iraq and Iran to Azerbaijan.'),
        ),
        'about': (
            _('About Us'),
            _('Years of experience in international road transportation, transit and logistics on the '
              'Iran–Turkey–Europe corridor, with a network of foreign carriers, forwarders and trained drivers.'),
        ),
        'contact': (
            _('Contact Us – Request a Transport Consultation'),
            _('Contact our operations team by phone, mobile or email, or send a transport consultation request '
              'with your origin, destination and cargo type.'),
        ),
    }


def page_seo(request, key, title=None, description=None, image=None):
    company = CompanyInfo.load()
    default_title, default_desc = _texts().get(key, ('', ''))
    brand = company.tr('short_name') if company else _('Ravan Seir Abrisham')
    title = title or default_title
    full_title = f'{title} | {brand}' if key != 'home' else f'{brand} | {title}'
    path = request.path
    alternates = []
    for code, _name in settings.LANGUAGES:
        alternates.append({'lang': code, 'url': settings.SITE_URL + translate_url(path, code)})
    return {
        'title': full_title,
        'description': (description or default_desc)[:300],
        'canonical': settings.SITE_URL + path,
        'alternates': alternates,
        'x_default': settings.SITE_URL + translate_url(path, settings.LANGUAGE_CODE),
        'image': image or settings.SITE_URL + static('images/og-image.png'),
        'locale': {'fa': 'fa_IR', 'en': 'en_US', 'tr': 'tr_TR'}[current_lang()],
        'type': 'website',
    }
