from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

IMAGE_VALIDATOR = FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'avif'])
COMPANY_CACHE_KEY = 'core:company'


LANG_CODES = ('fa', 'en', 'tr')
# When a text is missing in one language, show the next one (Turkish visitors read English first).
FALLBACKS = {'fa': ('fa', 'en'), 'en': ('en', 'fa'), 'tr': ('tr', 'en', 'fa')}


def current_lang():
    code = (get_language() or 'fa')[:2]
    return code if code in LANG_CODES else 'fa'


class Translated(models.Model):
    """
    Content stored once per language (`title_fa`, `title_en`, `title_tr`). `obj.tr('title')` returns the
    active language with a fallback (tr → en → fa, en → fa), so a missing text never leaves a hole.
    """

    class Meta:
        abstract = True

    def tr(self, field):
        for lang in FALLBACKS[current_lang()]:
            value = getattr(self, f'{field}_{lang}', '')
            if value:
                return value
        return ''

    def tr_lines(self, field):
        return [line.strip() for line in (self.tr(field) or '').splitlines() if line.strip()]


class CompanyInfo(Translated):
    """Single row: the company's official name, texts, contact details and key images."""

    name_fa = models.CharField(_('name (Persian)'), max_length=150)
    name_en = models.CharField(_('name (English)'), max_length=150)
    name_tr = models.CharField(_('name (Turkish)'), max_length=150, blank=True)
    short_name_fa = models.CharField(_('short name (Persian)'), max_length=60)
    short_name_en = models.CharField(_('short name (English)'), max_length=60)
    short_name_tr = models.CharField(_('short name (Turkish)'), max_length=60, blank=True)
    tagline_fa = models.CharField(_('tagline (Persian)'), max_length=200, blank=True)
    tagline_en = models.CharField(_('tagline (English)'), max_length=200, blank=True)
    tagline_tr = models.CharField(_('tagline (Turkish)'), max_length=200, blank=True)
    short_description_fa = models.TextField(_('short description (Persian)'))
    short_description_en = models.TextField(_('short description (English)'))
    short_description_tr = models.TextField(_('short description (Turkish)'), blank=True)
    description_fa = models.TextField(_('full description (Persian)'))
    description_en = models.TextField(_('full description (English)'))
    description_tr = models.TextField(_('full description (Turkish)'), blank=True)

    email = models.EmailField(_('email'))
    office_phone = models.CharField(_('office phone'), max_length=20)
    mobile = models.CharField(_('mobile'), max_length=20)
    address_fa = models.CharField(_('address (Persian)'), max_length=255, blank=True,
                                  help_text=_('Leave empty to hide the address everywhere.'))
    address_en = models.CharField(_('address (English)'), max_length=255, blank=True)
    address_tr = models.CharField(_('address (Turkish)'), max_length=255, blank=True)

    logo = models.FileField(_('logo'), upload_to='company/', blank=True, validators=[
        FileExtensionValidator(['svg', 'png', 'webp'])], help_text=_('Optional. SVG or PNG; replaces the built-in mark.'))
    hero_image = models.FileField(_('hero photo'), upload_to='company/', blank=True, validators=[IMAGE_VALIDATOR],
                                  help_text=_('Wide landscape photo of a truck on a highway (at least 2000 px wide, '
                                              'WebP or JPEG). Replaces the built-in hero illustration.'))
    about_image = models.FileField(_('introduction photo'), upload_to='company/', blank=True,
                                   validators=[IMAGE_VALIDATOR],
                                   help_text=_('Shown next to the company introduction. Replaces the illustration.'))

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('company information')
        verbose_name_plural = _('company information')

    def __str__(self):
        return self.name_en or self.name_fa

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(COMPANY_CACHE_KEY)

    def delete(self, *args, **kwargs):
        return  # the single row is edited, never deleted

    @classmethod
    def load(cls):
        obj = cache.get(COMPANY_CACHE_KEY)
        if obj is None:
            obj = cls.objects.filter(pk=1).first()
            if obj is not None:
                cache.set(COMPANY_CACHE_KEY, obj, 300)
        return obj

    @property
    def office_phone_tel(self):
        return _tel(self.office_phone)

    @property
    def mobile_tel(self):
        return _tel(self.mobile)


def _tel(number):
    """Iranian number → international tel: link (02188935889 → +982188935889)."""
    digits = ''.join(ch for ch in number if ch.isdigit())
    if digits.startswith('0'):
        digits = '98' + digits[1:]
    return '+' + digits
