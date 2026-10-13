from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from contact.forms import ContactForm
from core.seo import page_seo
from services.models import FleetVehicle, Route, Service

# Values and advantages are fixed wording from the company brief (no invented facts or numbers).
VALUES = [
    ('award', _('Experience'), _('Years of experience in road transportation and foreign transit.')),
    ('shield-check', _('Safety'), _('Careful handling and trained drivers for the safe carriage of goods.')),
    ('gauge', _('Speed'), _('Fast coordination of loading, documents and border crossings.')),
    ('eye', _('Transparency'), _('Clear communication and standard, transparent services.')),
    ('globe', _('International network'), _('Partnerships with foreign carriers and professional forwarders.')),
    ('users', _('Expert team'), _('A specialised operations team for planning and follow-up.')),
]

ADVANTAGES = [
    ('network', _('Extensive international network'),
     _('Cooperation with foreign transport companies and professional freight forwarders.')),
    ('steering', _('Trained drivers'), _('Professional drivers for the safe carriage of your goods.')),
    ('route', _('International route coverage'), _('Active on routes between Iran, Turkey, Europe and the region.')),
    ('stamp', _('Customs coordination'),
     _('Coordination with customs offices and the procedures for export and transit.')),
    ('eye', _('Transparent operations'), _('A focus on standard, transparent and accountable service.')),
]

PROCESS = [
    ('clipboard', _('Submit a request'), _('Tell us the origin, destination and type of cargo.')),
    ('search', _('Cargo and route review'), _('We assess the cargo, the best route and the right truck type.')),
    ('file', _('Transport and document coordination'), _('Loading, customs documents and transit paperwork are arranged.')),
    ('truck', _('Transportation and transit'), _('The truck travels the route and crosses the borders with our follow-up.')),
    ('package', _('Delivery'), _('Your cargo is delivered at the destination.')),
]


MAP_ROUTES = {'tr-ir', 'ir-tr', 'ir-eu', 'ir-iq', 'ir-az'}   # lines drawn on the route map


def route_context():
    routes = list(Route.objects.published())
    return {'routes': routes, 'route_keys': [r.key for r in routes if r.key in MAP_ROUTES]}


def border_count():
    transit = Service.objects.published().filter(slug='international-transit').first()
    return len(transit.tr_lines('points')) if transit else 0


def home(request):
    return render(request, 'pages/home.html', {
        **route_context(),
        'services': Service.objects.published(),
        'border_count': border_count(),
        'fleet': FleetVehicle.objects.published(),
        'values': VALUES,
        'advantages': ADVANTAGES,
        'process': PROCESS,
        'form': ContactForm(),
        'seo': page_seo(request, 'home'),
        'active_nav': 'home',
    })


def routes(request):
    return render(request, 'pages/routes.html', {
        **route_context(),
        'process': PROCESS,
        'transit_service': Service.objects.published().filter(slug='international-transit').first(),
        'seo': page_seo(request, 'routes'),
        'active_nav': 'routes',
    })


def about(request):
    return render(request, 'pages/about.html', {
        'values': VALUES,
        'advantages': ADVANTAGES,
        'fleet': FleetVehicle.objects.published(),
        'seo': page_seo(request, 'about'),
        'active_nav': 'about',
    })
