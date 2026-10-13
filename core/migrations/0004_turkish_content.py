"""Turkish company texts (editable in the admin panel)."""

from django.db import migrations


def seed(apps, schema_editor):
    CompanyInfo = apps.get_model('core', 'CompanyInfo')
    CompanyInfo.objects.filter(pk=1, name_tr='').update(
        name_tr='Ravan Seir Abrisham Uluslararası Taşımacılık',
        short_name_tr='Ravan Seir Abrisham',
        tagline_tr='Uluslararası taşımacılık: hızlı, güvenli ve güvenilir',
        short_description_tr=(
            'Ravan Seir Abrisham Uluslararası Taşımacılık, karayolu taşımacılığı, uluslararası transit ve lojistik '
            'hizmetlerinde yılların deneyimiyle İran–Türkiye–Avrupa güzergâhlarında faaliyet gösteren köklü ve aktif '
            'bir firmadır. Geniş yurt dışı iş ortağı ağımız, profesyonel sürücülerimiz ve uzman operasyon ekibimizle '
            'yükleri hızlı, güvenli ve tam şeffaflıkla taşıyoruz.'
        ),
        description_tr=(
            'Ravan Seir Abrisham Uluslararası Taşımacılık, karayolu taşımacılığı, uluslararası transit ve lojistik '
            'hizmetlerindeki yılların deneyimiyle İran–Türkiye–Avrupa güzergâhlarında aktif ve güvenilir bir firma '
            'olarak tanınmaktadır.\n'
            'Yurt dışındaki taşımacılık şirketleri, profesyonel forwarder’lar ve eğitimli sürücülerden oluşan geniş '
            'bir ağ ile her türlü yük için hızlı, güvenli ve ekonomik taşımacılık sunuyoruz.\n'
            'Amacımız, uluslararası taşımacılık ilkelerine dayanan standart ve şeffaf hizmetler sunmaktır.'
        ),
    )


class Migration(migrations.Migration):
    dependencies = [('core', '0003_turkish_fields')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
