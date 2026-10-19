"""Official addresses and extra phone lines supplied by the company (editable in the admin panel)."""

from django.db import migrations

VALUES = {
    'address_fa': 'تهران، خیابان طالقانی، نبش ویلا، ساختمان ۲۴۳، طبقه ۳',
    'address_en': '3rd Floor, Building 243, Corner of Villa St., Taleghani St., Tehran, Iran',
    'address_tr': 'Taleghani Caddesi, Villa Sokağı köşesi, Bina No. 243, Kat 3, Tahran, İran',
    'branch_address_fa': 'مرند، میدان امام حسین، طبقه فوقانی ترمینال، پلاک ۲۱۰',
    'branch_address_en': 'No. 210, Upper Floor of the Terminal, Imam Hossein Square, Marand, Iran',
    'branch_address_tr': 'İmam Hüseyin Meydanı, Terminal üst katı, No. 210, Marand, İran',
    'branch_phone': '0414226066',
    'work_phone': '0958866054',
}


def seed(apps, schema_editor):
    CompanyInfo = apps.get_model('core', 'CompanyInfo')
    company = CompanyInfo.objects.filter(pk=1).first()
    if company is None:
        return
    changed = []
    for field, value in VALUES.items():
        if not getattr(company, field):
            setattr(company, field, value)
            changed.append(field)
    if changed:
        company.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [('core', '0005_company_branch')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
