"""Persian pages live at the site root (/), English pages under /en/."""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import set_language

from core.sitemaps import ServiceSitemap, StaticSitemap
from core.views import healthz, robots_txt, vcard

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('robots.txt', robots_txt, name='robots'),
    path('healthz', healthz, name='healthz'),
    path('sitemap.xml', sitemap, {'sitemaps': {'pages': StaticSitemap, 'services': ServiceSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('i18n/setlang/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    path('services/', include('services.urls')),
    path('contact/', include('contact.urls')),
    path('contact-card.vcf', vcard, name='vcard'),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
