from django.db import migrations, models


def char(label, n):
    return models.CharField(blank=True, max_length=n, verbose_name=label)


def text(label, **kw):
    return models.TextField(blank=True, verbose_name=label, **kw)


class Migration(migrations.Migration):
    dependencies = [('services', '0002_seed_content')]

    operations = [
        migrations.AddField('service', 'title_tr', char('title (Turkish)', 120)),
        migrations.AddField('service', 'summary_tr', text('summary (Turkish)')),
        migrations.AddField('service', 'body_tr', text('details (Turkish)')),
        migrations.AddField('service', 'points_title_tr', char('list heading (Turkish)', 120)),
        migrations.AddField('service', 'points_tr', text('list items (Turkish)', help_text='One item per line.')),
        migrations.AddField('service', 'extra_title_tr', char('second list heading (Turkish)', 120)),
        migrations.AddField('service', 'extra_points_tr', text('second list items (Turkish)')),
        migrations.AddField('route', 'origin_tr', char('origin (Turkish)', 60)),
        migrations.AddField('route', 'destination_tr', char('destination (Turkish)', 60)),
        migrations.AddField('route', 'description_tr', char('description (Turkish)', 255)),
        migrations.AddField('fleetvehicle', 'name_tr', char('type (Turkish)', 80)),
        migrations.AddField('fleetvehicle', 'description_tr', text('description (Turkish)')),
    ]
