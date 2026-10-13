import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from core.seo import page_seo

from .forms import ContactForm

logger = logging.getLogger('contact')


def client_ip(request):
    return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')


def wants_json(request):
    return 'application/json' in request.headers.get('Accept', '')


def rate_limited(ip):
    key = f'contact:rate:{ip}'
    cache.add(key, 0, 60 * 60)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, 60 * 60)
        count = 1
    return count > settings.CONTACT_RATE_LIMIT


def notify_staff(obj):
    if not settings.CONTACT_NOTIFY_EMAILS:
        return
    body = '\n'.join(f'{label}: {value}' for label, value in [
        ('Name', obj.full_name), ('Phone', obj.phone), ('Email', obj.email or '-'),
        ('Origin', obj.origin or '-'), ('Destination', obj.destination or '-'),
        ('Cargo', obj.cargo_type or '-'), ('Language', obj.language), ('', ''), ('Message', obj.message or '-'),
    ])
    try:
        send_mail(f'New transport consultation request – {obj.full_name}', body,
                  settings.DEFAULT_FROM_EMAIL, settings.CONTACT_NOTIFY_EMAILS)
    except Exception:  # noqa: BLE001 – the request is saved; email is best effort
        logger.exception('Could not send the notification email for contact request %s', obj.pk)


@require_http_methods(['GET', 'POST'])
def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        success_text = _('Thank you. Your request has been received and our team will contact you shortly.')
        if rate_limited(client_ip(request)):
            error = _('Too many requests from your connection. Please try again later or call us directly.')
            if wants_json(request):
                return JsonResponse({'ok': False, 'message': error}, status=429)
            messages.error(request, error)
            return redirect(reverse('contact:page') + '#contact-form')
        if form.is_valid():
            if form.is_spam():
                # Pretend it worked so bots learn nothing.
                return JsonResponse({'ok': True, 'message': success_text}) if wants_json(request) \
                    else redirect(reverse('contact:page') + '?sent=1#contact-form')
            obj = form.save(commit=False)
            obj.language = (get_language() or 'fa')[:5]
            obj.ip_address = client_ip(request)
            obj.user_agent = request.headers.get('User-Agent', '')[:255]
            obj.save()
            notify_staff(obj)
            logger.info('Contact request %s saved', obj.pk)
            if wants_json(request):
                return JsonResponse({'ok': True, 'message': success_text})
            messages.success(request, success_text)
            return redirect(reverse('contact:page') + '#contact-form')
        if wants_json(request):
            return JsonResponse({
                'ok': False,
                'message': _('Please check the highlighted fields.'),
                'errors': {field: [str(e) for e in errs] for field, errs in form.errors.items()},
            })   # 200 + ok:false, so browsers don't log an expected validation result as a network error
    return render(request, 'pages/contact.html', {
        'form': form,
        'seo': page_seo(request, 'contact'),
        'active_nav': 'contact',
    }, status=400 if form.is_bound and form.errors else 200)
