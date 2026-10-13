from django.shortcuts import get_object_or_404, render

from contact.forms import ContactForm
from core.seo import page_seo

from .models import FleetVehicle, Service


def service_list(request):
    return render(request, 'pages/services.html', {
        'services': Service.objects.published(),
        'fleet': FleetVehicle.objects.published(),
        'seo': page_seo(request, 'services'),
        'active_nav': 'services',
    })


def service_detail(request, slug):
    service = get_object_or_404(Service.objects.published(), slug=slug)
    others = Service.objects.published().exclude(pk=service.pk)
    return render(request, 'pages/service_detail.html', {
        'service': service,
        'others': others,
        'form': ContactForm(),
        'seo': page_seo(request, 'services', title=service.tr('title'), description=service.tr('summary')),
        'active_nav': 'services',
    })
