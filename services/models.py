from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import IMAGE_VALIDATOR, Translated


class OrderedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_active=True)


class Service(Translated):
    ICONS = [
        ('truck', _('Truck')),
        ('route', _('Route / transit')),
        ('container', _('Container / forwarding')),
        ('export', _('Export')),
        ('consult', _('Consulting')),
        ('customs', _('Customs')),
    ]

    slug = models.SlugField(_('URL name'), unique=True, help_text=_('English, e.g. road-transportation'))
    icon = models.CharField(_('icon'), max_length=20, choices=ICONS, default='truck')
    title_fa = models.CharField(_('title (Persian)'), max_length=120)
    title_en = models.CharField(_('title (English)'), max_length=120)
    title_tr = models.CharField(_('title (Turkish)'), max_length=120, blank=True)
    summary_fa = models.TextField(_('summary (Persian)'))
    summary_en = models.TextField(_('summary (English)'))
    summary_tr = models.TextField(_('summary (Turkish)'), blank=True)
    body_fa = models.TextField(_('details (Persian)'), blank=True)
    body_en = models.TextField(_('details (English)'), blank=True)
    body_tr = models.TextField(_('details (Turkish)'), blank=True)
    points_title_fa = models.CharField(_('list heading (Persian)'), max_length=120, blank=True)
    points_title_en = models.CharField(_('list heading (English)'), max_length=120, blank=True)
    points_title_tr = models.CharField(_('list heading (Turkish)'), max_length=120, blank=True)
    points_fa = models.TextField(_('list items (Persian)'), blank=True, help_text=_('One item per line.'))
    points_en = models.TextField(_('list items (English)'), blank=True, help_text=_('One item per line.'))
    points_tr = models.TextField(_('list items (Turkish)'), blank=True, help_text=_('One item per line.'))
    extra_title_fa = models.CharField(_('second list heading (Persian)'), max_length=120, blank=True)
    extra_title_en = models.CharField(_('second list heading (English)'), max_length=120, blank=True)
    extra_title_tr = models.CharField(_('second list heading (Turkish)'), max_length=120, blank=True)
    extra_points_fa = models.TextField(_('second list items (Persian)'), blank=True)
    extra_points_en = models.TextField(_('second list items (English)'), blank=True)
    extra_points_tr = models.TextField(_('second list items (Turkish)'), blank=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('published'), default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.title_en or self.title_fa

    def get_absolute_url(self):
        return reverse('services:detail', args=[self.slug])

    @property
    def number(self):
        return f'{self.order:02d}'


class Route(Translated):
    origin_fa = models.CharField(_('origin (Persian)'), max_length=60)
    origin_en = models.CharField(_('origin (English)'), max_length=60)
    origin_tr = models.CharField(_('origin (Turkish)'), max_length=60, blank=True)
    origin_code = models.CharField(_('origin map node'), max_length=3,
                                   help_text=_('Node on the route map: TR, IR, EU, IQ or AZ.'))
    destination_fa = models.CharField(_('destination (Persian)'), max_length=60)
    destination_en = models.CharField(_('destination (English)'), max_length=60)
    destination_tr = models.CharField(_('destination (Turkish)'), max_length=60, blank=True)
    destination_code = models.CharField(_('destination map node'), max_length=3)
    description_fa = models.CharField(_('description (Persian)'), max_length=255, blank=True)
    description_en = models.CharField(_('description (English)'), max_length=255, blank=True)
    description_tr = models.CharField(_('description (Turkish)'), max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('published'), default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('route')
        verbose_name_plural = _('active routes')

    def __str__(self):
        return f'{self.origin_en} → {self.destination_en}'

    @property
    def key(self):
        return f'{self.origin_code}-{self.destination_code}'.lower()


class FleetVehicle(Translated):
    ILLUSTRATIONS = [
        ('curtain', _('Curtain-side')),
        ('tanker', _('Tanker')),
        ('reefer', _('Refrigerated')),
        ('transit', _('Transit / container')),
    ]

    illustration = models.CharField(_('built-in illustration'), max_length=10, choices=ILLUSTRATIONS)
    name_fa = models.CharField(_('type (Persian)'), max_length=80)
    name_en = models.CharField(_('type (English)'), max_length=80)
    name_tr = models.CharField(_('type (Turkish)'), max_length=80, blank=True)
    description_fa = models.TextField(_('description (Persian)'))
    description_en = models.TextField(_('description (English)'))
    description_tr = models.TextField(_('description (Turkish)'), blank=True)
    image = models.FileField(_('photo'), upload_to='fleet/', blank=True, validators=[IMAGE_VALIDATOR],
                             help_text=_('Optional real photo (landscape, ~1200 px). Replaces the illustration.'))
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('published'), default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('vehicle type')
        verbose_name_plural = _('fleet')

    def __str__(self):
        return self.name_en or self.name_fa
