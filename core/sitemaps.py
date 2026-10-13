from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from services.models import Service


class StaticSitemap(Sitemap):
    i18n = True
    alternates = True
    x_default = True
    changefreq = 'monthly'

    def items(self):
        return ['pages:home', 'services:list', 'pages:routes', 'pages:about', 'contact:page']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'pages:home' else 0.8


class ServiceSitemap(Sitemap):
    i18n = True
    alternates = True
    x_default = True
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.published()
