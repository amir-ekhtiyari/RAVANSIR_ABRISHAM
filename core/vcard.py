"""vCard (contact card) built only from the stored company details – used for the QR code and the .vcf download."""

from django.conf import settings


def _esc(value):
    return str(value).replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')


def company_vcard(company, compact=False):
    """Full card for the .vcf download; `compact` (for QR codes) keeps the short name, phones, email and site only,
    so the code stays small enough to scan easily."""
    if company is None:
        return ''
    name = company.tr('short_name') if compact else company.tr('name')
    lines = ['BEGIN:VCARD', 'VERSION:3.0', f'N:{_esc(name)};;;;', f'FN:{_esc(name)}']
    if not compact:
        lines.append(f'ORG:{_esc(name)}')
    phones = [
        ('WORK,VOICE', company.office_phone_tel),
        ('CELL', company.mobile_tel),
        ('WORK', company.work_phone_tel),
        ('WORK', company.branch_phone_tel),
    ]
    lines += [f'TEL;TYPE={kind}:{tel}' for kind, tel in phones if tel]
    if company.email:
        lines.append(f'EMAIL;TYPE=INTERNET:{company.email}')
    for address in () if compact else (company.tr('address'), company.tr('branch_address')):
        if address:
            lines.append(f'ADR;TYPE=WORK:;;{_esc(address)};;;;')
    lines += [f'URL:{settings.SITE_URL}/', 'END:VCARD']
    return '\r\n'.join(lines) + '\r\n'
