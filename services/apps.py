from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
    verbose_name = _('Services, routes and fleet')

    def ready(self):
        from django.core.cache import cache
        from django.db.models.signals import post_delete, post_save

        from .models import FleetVehicle, Route, Service

        def clear(**kwargs):
            cache.delete_many(['core:footer:services', 'core:footer:routes'])

        for model in (Service, Route, FleetVehicle):
            post_save.connect(clear, sender=model, dispatch_uid=f'clear-footer-{model.__name__}')
            post_delete.connect(clear, sender=model, dispatch_uid=f'clear-footer-del-{model.__name__}')
