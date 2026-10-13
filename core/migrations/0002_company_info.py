"""The official company information from the brief (editable in the admin panel)."""

from django.db import migrations


def seed(apps, schema_editor):
    CompanyInfo = apps.get_model('core', 'CompanyInfo')
    CompanyInfo.objects.update_or_create(pk=1, defaults={
        'name_fa': 'شرکت حمل‌ونقل بین‌المللی روان سیر ابریشم',
        'name_en': 'Ravan Seir Abrisham International Transportation',
        'short_name_fa': 'روان سیر ابریشم',
        'short_name_en': 'Ravan Seir Abrisham',
        'tagline_fa': 'حمل‌ونقل بین‌المللی، سریع، ایمن و مطمئن',
        'tagline_en': 'International transportation – fast, safe and reliable',
        'short_description_fa': (
            'شرکت حمل‌ونقل بین‌المللی روان سیر ابریشم با سال‌ها تجربه در حوزه حمل‌ونقل جاده‌ای، ترانزیت خارجی و '
            'خدمات لجستیک، یکی از شرکت‌های معتبر و فعال در مسیرهای ایران–ترکیه–اروپا است. ما با تکیه بر شبکه گسترده '
            'شرکای خارجی، رانندگان حرفه‌ای و تیم متخصص عملیات، حمل کالا را با سرعت، امنیت و شفافیت کامل انجام می‌دهیم.'
        ),
        'short_description_en': (
            'Ravan Seir Abrisham International Transportation has years of experience in road transportation, foreign '
            'transit and logistics services, and is an established, active carrier on the Iran–Turkey–Europe routes. '
            'Backed by a wide network of foreign partners, professional drivers and a specialised operations team, we '
            'move cargo quickly, safely and with full transparency.'
        ),
        'description_fa': (
            'شرکت حمل‌ونقل بین‌المللی روان سیر ابریشم با سال‌ها تجربه در حوزه حمل‌ونقل جاده‌ای، ترانزیت خارجی و '
            'خدمات لجستیک، به‌عنوان یکی از شرکت‌های فعال و قابل‌اعتماد در مسیرهای ایران–ترکیه–اروپا شناخته می‌شود.\n'
            'ما با همکاری شبکه گسترده‌ای از شرکت‌های حمل خارجی، فورواردرهای حرفه‌ای و رانندگان آموزش‌دیده، امکان حمل '
            'سریع، ایمن و مقرون‌به‌صرفه انواع کالا را فراهم کرده‌ایم.\n'
            'هدف ما ارائه خدمات استاندارد، شفاف و مبتنی بر اصول بین‌المللی حمل‌ونقل است.'
        ),
        'description_en': (
            'With years of experience in road transportation, foreign transit and logistics, Ravan Seir Abrisham '
            'International Transportation is known as an active and dependable carrier on the Iran–Turkey–Europe '
            'routes.\n'
            'Together with a wide network of foreign transport companies, professional freight forwarders and trained '
            'drivers, we offer fast, safe and cost-effective transportation for all kinds of cargo.\n'
            'Our goal is to deliver standard, transparent services built on international transportation practice.'
        ),
        'email': 'tfahimi54@gmail.com',
        'office_phone': '02188935889',
        'mobile': '09144918300',
    })


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
