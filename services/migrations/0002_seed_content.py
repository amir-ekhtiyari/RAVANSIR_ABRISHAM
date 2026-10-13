"""Initial content from the company brief. Everything here can be edited later in the admin panel."""

from django.db import migrations

SERVICES = [
    {
        'slug': 'international-road-transportation', 'icon': 'truck', 'order': 1,
        'title_fa': 'حمل‌ونقل جاده‌ای بین‌المللی',
        'title_en': 'International Road Transportation',
        'summary_fa': 'حمل کالا از ترکیه، اروپا، آسیای میانه و کشورهای منطقه با انواع کامیون چادری، تانکر، یخچال‌دار و ترانزیتی.',
        'summary_en': 'Road freight from Turkey, Europe, Central Asia and neighbouring countries, with curtain-side, '
                      'tanker, refrigerated and transit trucks.',
        'body_fa': 'حمل جاده‌ای ستون اصلی فعالیت ماست. بسته به نوع کالا، مسیر و زمان مورد نیاز، ناوگان مناسب را انتخاب '
                   'می‌کنیم و حمل را از بارگیری در مبدأ تا تحویل در مقصد پیگیری می‌کنیم.',
        'body_en': 'Road freight is the core of our work. We match the right truck to your cargo, route and timeline, '
                   'and follow the shipment from loading at origin to delivery at destination.',
        'points_title_fa': 'مبدأهای حمل', 'points_title_en': 'Origins we serve',
        'points_fa': 'ترکیه\nاروپا\nآسیای میانه\nکشورهای منطقه',
        'points_en': 'Turkey\nEurope\nCentral Asia\nNeighbouring countries',
        'extra_title_fa': 'انواع ناوگان', 'extra_title_en': 'Truck types',
        'extra_points_fa': 'کامیون چادری (کرتین‌ساید)\nتانکر\nکامیون یخچال‌دار\nکامیون ترانزیتی',
        'extra_points_en': 'Curtain-side trucks\nTanker trucks\nRefrigerated trucks\nTransit trucks',
    },
    {
        'slug': 'international-transit', 'icon': 'route', 'order': 2,
        'title_fa': 'ترانزیت خارجی',
        'title_en': 'International Transit',
        'summary_fa': 'انجام عملیات ترانزیت خارجی از مرزهای بازرگان، رازی، سرو و جلفا؛ از هماهنگی گمرکی تا اسناد ترانزیت.',
        'summary_en': 'Foreign transit operations through the Bazargan, Razi, Serow and Jolfa borders – from customs '
                      'coordination to transit documents.',
        'body_fa': 'عبور کالای ترانزیتی از خاک ایران نیازمند هماهنگی دقیق اسناد و عملیات مرزی است. تیم عملیات ما این '
                   'مراحل را هماهنگ و پیگیری می‌کند تا محموله بدون توقف غیرضروری مسیر خود را ادامه دهد.',
        'body_en': 'Moving transit cargo across Iran depends on precise paperwork and border operations. Our operations '
                   'team coordinates and follows up each step so the shipment keeps moving without unnecessary stops.',
        'points_title_fa': 'مرزهای عملیاتی', 'points_title_en': 'Border crossings',
        'points_fa': 'بازرگان\nرازی\nسرو\nجلفا',
        'points_en': 'Bazargan\nRazi\nSerow\nJolfa',
        'extra_title_fa': 'شامل', 'extra_title_en': 'Including',
        'extra_points_fa': 'هماهنگی گمرکی\nبررسی و کنترل مدارک\nعملیات سامانه EPL\nتنظیم اسناد ترانزیت\nعملیات مرزی',
        'extra_points_en': 'Customs coordination\nDocument verification\nEPL system operations\n'
                           'Transit documentation\nBorder operations',
    },
    {
        'slug': 'freight-forwarding', 'icon': 'container', 'order': 3,
        'title_fa': 'فورواردرینگ',
        'title_en': 'Freight Forwarding',
        'summary_fa': 'ارائه خدمات حرفه‌ای فورواردرینگ و هماهنگی حمل بین‌المللی کالا.',
        'summary_en': 'Professional freight forwarding and coordination of international cargo movements.',
        'body_fa': 'با تکیه بر شبکه شرکای خارجی و فورواردرهای حرفه‌ای، حمل بین‌المللی کالای شما را برنامه‌ریزی و '
                   'هماهنگ می‌کنیم تا یک طرف پاسخ‌گو برای کل مسیر داشته باشید.',
        'body_en': 'Working with our network of foreign partners and professional forwarders, we plan and coordinate '
                   'your international shipment so you have one accountable partner for the whole journey.',
    },
    {
        'slug': 'export-transportation', 'icon': 'export', 'order': 4,
        'title_fa': 'حمل صادراتی',
        'title_en': 'Export Transportation',
        'summary_fa': 'هماهنگی کامل با گمرکات کشور برای صادرات کالاهای ایرانی به ترکیه، اروپا و کشورهای منطقه.',
        'summary_en': 'Full coordination with Iranian customs for exporting Iranian goods to Turkey, Europe and '
                      'neighbouring countries.',
        'body_fa': 'از هماهنگی با گمرک مبدأ تا رسیدن کالا به مقصد خارجی، فرایند حمل صادراتی را برای صادرکنندگان ایرانی '
                   'ساده و قابل پیگیری می‌کنیم.',
        'body_en': 'From coordination with the customs office of origin to arrival at the foreign destination, we make '
                   'export transportation simple and traceable for Iranian exporters.',
        'points_title_fa': 'مقصدها', 'points_title_en': 'Destinations',
        'points_fa': 'ترکیه\nاروپا\nکشورهای منطقه',
        'points_en': 'Turkey\nEurope\nNeighbouring countries',
    },
    {
        'slug': 'transportation-customs-consulting', 'icon': 'consult', 'order': 5,
        'title_fa': 'مشاوره حمل‌ونقل و گمرک',
        'title_en': 'Transportation & Customs Consulting',
        'summary_fa': 'مشاوره تخصصی در زمینه حمل‌ونقل بین‌المللی، فرایندهای گمرکی، ترانزیت، لجستیک صادرات، انتخاب مسیر و مدارک.',
        'summary_en': 'Specialist advice on international transportation, customs procedures, transit, export logistics, '
                      'route selection and documentation.',
        'body_fa': 'پیش از ارسال کالا، با شما درباره بهترین مسیر، نوع ناوگان، مدارک لازم و مراحل گمرکی گفت‌وگو می‌کنیم '
                   'تا با دید روشن تصمیم بگیرید.',
        'body_en': 'Before your cargo moves, we talk you through the best route, the right truck type, the documents '
                   'you need and the customs steps, so you can decide with a clear picture.',
        'points_title_fa': 'حوزه‌های مشاوره', 'points_title_en': 'Consulting areas',
        'points_fa': 'حمل‌ونقل بین‌المللی\nفرایندهای گمرکی\nترانزیت\nلجستیک صادرات\nانتخاب مسیر\nمدارک و اسناد حمل',
        'points_en': 'International transportation\nCustoms procedures\nTransit\nExport logistics\nRoute selection\n'
                     'Documentation',
    },
]

ROUTES = [
    ('ترکیه', 'Turkey', 'TR', 'ایران', 'Iran', 'IR',
     'حمل کالا از ترکیه به ایران', 'Road freight from Turkey into Iran'),
    ('ایران', 'Iran', 'IR', 'ترکیه', 'Turkey', 'TR',
     'حمل کالا و صادرات از ایران به ترکیه', 'Exports and road freight from Iran to Turkey'),
    ('ایران', 'Iran', 'IR', 'اروپا', 'Europe', 'EU',
     'حمل جاده‌ای کالا از ایران به اروپا', 'Road freight from Iran to Europe'),
    ('ایران', 'Iran', 'IR', 'عراق', 'Iraq', 'IQ',
     'حمل کالا از ایران به عراق', 'Road freight from Iran to Iraq'),
    ('ایران', 'Iran', 'IR', 'آذربایجان', 'Azerbaijan', 'AZ',
     'حمل کالا از ایران به جمهوری آذربایجان', 'Road freight from Iran to Azerbaijan'),
]

FLEET = [
    ('curtain', 'کامیون چادری (کرتین‌ساید)', 'Curtain-side truck',
     'برای حمل عمومی کالاهای بسته‌بندی‌شده و پالتی، با امکان بارگیری از کناره‌ها.',
     'For general packaged and palletised cargo, with loading from the sides.'),
    ('tanker', 'تانکر', 'Tanker',
     'برای حمل محموله‌های مایع به‌صورت فله.',
     'For liquid cargo carried in bulk.'),
    ('reefer', 'کامیون یخچال‌دار', 'Refrigerated truck',
     'برای کالاهایی که در طول مسیر به دمای کنترل‌شده نیاز دارند.',
     'For goods that need a controlled temperature throughout the journey.'),
    ('transit', 'کامیون ترانزیتی', 'Transit truck',
     'برای عملیات ترانزیت خارجی و عبور کالا از مرزهای کشور.',
     'For foreign transit operations and cross-border movements through Iran.'),
]


def seed(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Route = apps.get_model('services', 'Route')
    FleetVehicle = apps.get_model('services', 'FleetVehicle')
    for data in SERVICES:
        Service.objects.update_or_create(slug=data['slug'], defaults=data)
    for i, (ofa, oen, oc, dfa, den, dc, desc_fa, desc_en) in enumerate(ROUTES, start=1):
        Route.objects.get_or_create(origin_code=oc, destination_code=dc, defaults={
            'origin_fa': ofa, 'origin_en': oen, 'destination_fa': dfa, 'destination_en': den,
            'description_fa': desc_fa, 'description_en': desc_en, 'order': i})
    for i, (kind, nfa, nen, dfa, den) in enumerate(FLEET, start=1):
        FleetVehicle.objects.get_or_create(illustration=kind, defaults={
            'name_fa': nfa, 'name_en': nen, 'description_fa': dfa, 'description_en': den, 'order': i})


class Migration(migrations.Migration):
    dependencies = [('services', '0001_initial')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
