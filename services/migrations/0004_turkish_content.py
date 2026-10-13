"""Turkish versions of the initial services, routes and fleet (editable in the admin panel)."""

from django.db import migrations

SERVICES = {
    'international-road-transportation': {
        'title_tr': 'Uluslararası Karayolu Taşımacılığı',
        'summary_tr': 'Türkiye, Avrupa, Orta Asya ve bölge ülkelerinden tenteli, tanker, frigorifik ve transit '
                      'tırlarla yük taşımacılığı.',
        'body_tr': 'Karayolu taşımacılığı işimizin temelidir. Yükünüze, güzergâhınıza ve zaman planınıza uygun aracı '
                   'seçiyor, sevkiyatı çıkış noktasındaki yüklemeden varış noktasındaki teslimata kadar takip '
                   'ediyoruz.',
        'points_title_tr': 'Çıkış noktaları',
        'points_tr': 'Türkiye\nAvrupa\nOrta Asya\nBölge ülkeleri',
        'extra_title_tr': 'Araç tipleri',
        'extra_points_tr': 'Tenteli tırlar\nTankerler\nFrigorifik tırlar\nTransit tırlar',
    },
    'international-transit': {
        'title_tr': 'Uluslararası Transit',
        'summary_tr': 'Bazargan, Razi, Serow ve Culfa sınır kapılarından transit operasyonları – gümrük '
                      'koordinasyonundan transit belgelerine kadar.',
        'body_tr': 'Transit yükün İran üzerinden geçişi, belgelerin ve sınır işlemlerinin titizlikle koordine '
                   'edilmesini gerektirir. Operasyon ekibimiz her adımı koordine edip takip eder; böylece sevkiyat '
                   'gereksiz beklemeler olmadan yoluna devam eder.',
        'points_title_tr': 'Sınır kapıları',
        'points_tr': 'Bazargan\nRazi\nSerow\nCulfa',
        'extra_title_tr': 'Kapsam',
        'extra_points_tr': 'Gümrük koordinasyonu\nBelge kontrolü\nEPL sistemi işlemleri\nTransit belgeleri\n'
                           'Sınır operasyonları',
    },
    'freight-forwarding': {
        'title_tr': 'Freight Forwarding',
        'summary_tr': 'Profesyonel freight forwarding hizmetleri ve uluslararası yük taşımacılığının koordinasyonu.',
        'body_tr': 'Yabancı iş ortaklarımız ve profesyonel forwarder ağımızla uluslararası sevkiyatınızı planlıyor '
                   've koordine ediyoruz; tüm yolculuk boyunca tek bir sorumlu muhatabınız oluyor.',
    },
    'export-transportation': {
        'title_tr': 'İhracat Taşımacılığı',
        'summary_tr': 'İran mallarının Türkiye, Avrupa ve bölge ülkelerine ihracatı için İran gümrükleriyle tam '
                      'koordinasyon.',
        'body_tr': 'Çıkış gümrüğüyle koordinasyondan yükün yurt dışındaki varış noktasına ulaşmasına kadar, İranlı '
                   'ihracatçılar için ihracat taşımacılığını sade ve takip edilebilir hâle getiriyoruz.',
        'points_title_tr': 'Varış noktaları',
        'points_tr': 'Türkiye\nAvrupa\nBölge ülkeleri',
    },
    'transportation-customs-consulting': {
        'title_tr': 'Taşımacılık ve Gümrük Danışmanlığı',
        'summary_tr': 'Uluslararası taşımacılık, gümrük süreçleri, transit, ihracat lojistiği, güzergâh seçimi ve '
                      'belgeler konusunda uzman danışmanlık.',
        'body_tr': 'Yükünüz yola çıkmadan önce en uygun güzergâhı, doğru araç tipini, gerekli belgeleri ve gümrük '
                   'adımlarını sizinle birlikte değerlendiriyoruz; böylece net bir tabloyla karar verebilirsiniz.',
        'points_title_tr': 'Danışmanlık alanları',
        'points_tr': 'Uluslararası taşımacılık\nGümrük süreçleri\nTransit\nİhracat lojistiği\nGüzergâh seçimi\n'
                     'Belgeler',
    },
}

PLACES = {'TR': 'Türkiye', 'IR': 'İran', 'EU': 'Avrupa', 'IQ': 'Irak', 'AZ': 'Azerbaycan'}
ROUTE_DESC = {
    ('TR', 'IR'): 'Türkiye’den İran’a karayolu taşımacılığı',
    ('IR', 'TR'): 'İran’dan Türkiye’ye ihracat ve karayolu taşımacılığı',
    ('IR', 'EU'): 'İran’dan Avrupa’ya karayolu taşımacılığı',
    ('IR', 'IQ'): 'İran’dan Irak’a karayolu taşımacılığı',
    ('IR', 'AZ'): 'İran’dan Azerbaycan’a karayolu taşımacılığı',
}

FLEET = {
    'curtain': ('Tenteli tır', 'Paketli ve paletli genel yükler için; yanlardan yükleme imkânı sunar.'),
    'tanker': ('Tanker', 'Dökme sıvı yükler için.'),
    'reefer': ('Frigorifik tır', 'Yolculuk boyunca kontrollü sıcaklık gerektiren ürünler için.'),
    'transit': ('Transit tır', 'Uluslararası transit operasyonları ve İran üzerinden sınır geçişleri için.'),
}


def seed(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Route = apps.get_model('services', 'Route')
    FleetVehicle = apps.get_model('services', 'FleetVehicle')
    for slug, data in SERVICES.items():
        Service.objects.filter(slug=slug, title_tr='').update(**data)
    for route in Route.objects.filter(origin_tr=''):
        route.origin_tr = PLACES.get(route.origin_code, '')
        route.destination_tr = PLACES.get(route.destination_code, '')
        route.description_tr = ROUTE_DESC.get((route.origin_code, route.destination_code), '')
        route.save()
    for kind, (name, desc) in FLEET.items():
        FleetVehicle.objects.filter(illustration=kind, name_tr='').update(name_tr=name, description_tr=desc)


class Migration(migrations.Migration):
    dependencies = [('services', '0003_turkish_fields')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
