from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FleetVehicle, Route, Service

LANGS = (('fa', _('Persian')), ('en', _('English')), ('tr', _('Turkish')))


def per_language(*fields):
    """One collapsible-free fieldset per language with the same fields (title_fa, title_en, title_tr …)."""
    return tuple((label, {'fields': tuple(f'{f}_{code}' for f in fields)}) for code, label in LANGS)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_fa', 'title_en', 'title_tr', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title_en',)}
    search_fields = ('title_fa', 'title_en', 'title_tr')
    fieldsets = ((None, {'fields': ('slug', 'icon', 'order', 'is_active')}),) + per_language(
        'title', 'summary', 'body', 'points_title', 'points', 'extra_title', 'extra_points')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'origin_fa', 'destination_fa', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = ((None, {'fields': ('origin_code', 'destination_code', 'order', 'is_active')}),) + per_language(
        'origin', 'destination', 'description')


@admin.register(FleetVehicle)
class FleetVehicleAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'illustration', 'has_photo', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = ((None, {'fields': ('illustration', 'image', 'order', 'is_active')}),) + per_language(
        'name', 'description')

    @admin.display(boolean=True, description=_('photo'))
    def has_photo(self, obj):
        return bool(obj.image)
