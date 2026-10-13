from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=86400)
def robots_txt(request):
    lines = [
        'User-agent: *',
        f'Disallow: /{settings.ADMIN_URL}',
        'Disallow: /media/company/',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')


def page_not_found(request, exception):
    from django.utils.translation import gettext as _

    from .seo import page_seo
    seo = page_seo(request, 'home', title=_('Page not found'))
    seo['title'] = _('Page not found')
    return render(request, '404.html', {'seo': seo}, status=404)


def server_error(request):
    return render(request, '500.html', status=500)
