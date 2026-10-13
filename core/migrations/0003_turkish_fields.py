from django.db import migrations, models


def field(kind, label, **kw):
    cls = models.TextField if kind == 'text' else models.CharField
    return cls(blank=True, verbose_name=label, **kw)


class Migration(migrations.Migration):
    dependencies = [('core', '0002_company_info')]

    operations = [
        migrations.AddField('companyinfo', 'name_tr', field('char', 'name (Turkish)', max_length=150)),
        migrations.AddField('companyinfo', 'short_name_tr', field('char', 'short name (Turkish)', max_length=60)),
        migrations.AddField('companyinfo', 'tagline_tr', field('char', 'tagline (Turkish)', max_length=200)),
        migrations.AddField('companyinfo', 'short_description_tr', field('text', 'short description (Turkish)')),
        migrations.AddField('companyinfo', 'description_tr', field('text', 'full description (Turkish)')),
        migrations.AddField('companyinfo', 'address_tr', field('char', 'address (Turkish)', max_length=255)),
    ]
