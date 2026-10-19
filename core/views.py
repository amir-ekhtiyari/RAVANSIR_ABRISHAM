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


@require_GET
def healthz(request):
    """Liveness/readiness probe for Docker and the reverse proxy: checks the database connection."""
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:  # noqa: BLE001 – any database error means "not ready"
        return HttpResponse('database unavailable', status=503, content_type='text/plain')
    return HttpResponse('ok', content_type='text/plain')


@require_GET
def vcard(request):
    """Company contact card (.vcf) – opens straight in the phone's contacts app."""
    from .models import CompanyInfo
    from .vcard import company_vcard
    response = HttpResponse(company_vcard(CompanyInfo.load()), content_type='text/vcard; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ravan-seir-abrisham.vcf"'
    return response


def page_not_found(request, exception):
    from django.utils.translation import gettext as _

    from .seo import page_seo
    seo = page_seo(request, 'home', title=_('Page not found'))
    seo['title'] = _('Page not found')
    return render(request, '404.html', {'seo': seo}, status=404)


def server_error(request):
    return render(request, '500.html', status=500)
