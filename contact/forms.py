import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactRequest

PERSIAN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
PHONE_RE = re.compile(r'^\+?\d{8,15}$')


def normalise_digits(value):
    return (value or '').translate(PERSIAN_DIGITS)


class ContactForm(forms.ModelForm):
    # Honeypot: hidden from people, filled in by most bots.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'tabindex': '-1', 'autocomplete': 'off', 'aria-hidden': 'true'}))

    class Meta:
        model = ContactRequest
        fields = ['full_name', 'phone', 'email', 'origin', 'destination', 'cargo_type', 'message']
        labels = {
            'full_name': _('Full name'),
            'phone': _('Phone number'),
            'email': _('Email'),
            'origin': _('Origin'),
            'destination': _('Destination'),
            'cargo_type': _('Cargo type'),
            'message': _('Message'),
        }
        help_texts = {
            'email': _('Optional'),
            'cargo_type': _('For example: textiles, food products, chemicals, machinery'),
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel', 'inputmode': 'tel', 'dir': 'ltr'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'dir': 'ltr'}),
            'origin': forms.TextInput(attrs={'list': 'place-suggestions'}),
            'destination': forms.TextInput(attrs={'list': 'place-suggestions'}),
            'cargo_type': forms.TextInput(),
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        error_messages = {
            'full_name': {'required': _('Please enter your name.')},
            'phone': {'required': _('Please enter a phone number so we can call you back.')},
            'email': {'invalid': _('Please enter a valid email address.')},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'website':
                continue
            ids = [f'id_{name}_error']
            if field.help_text and name != 'email':
                ids.insert(0, f'id_{name}_help')
            field.widget.attrs['aria-describedby'] = ' '.join(ids)
            if field.required:
                field.widget.attrs['aria-required'] = 'true'
            if self.is_bound and name in self.errors:
                field.widget.attrs['aria-invalid'] = 'true'

    def clean_full_name(self):
        name = ' '.join(self.cleaned_data['full_name'].split())
        if len(name) < 2:
            raise forms.ValidationError(_('Please enter your name.'))
        return name

    def clean_phone(self):
        raw = normalise_digits(self.cleaned_data['phone'])
        phone = re.sub(r'[\s\-().]', '', raw)
        if phone.startswith('00'):
            phone = '+' + phone[2:]
        if not PHONE_RE.match(phone):
            raise forms.ValidationError(_('Please enter a valid phone number, e.g. 0912 345 6789.'))
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if message.count('http://') + message.count('https://') > 2:
            raise forms.ValidationError(_('Please remove the links from your message.'))
        return message

    def is_spam(self):
        return bool(self.cleaned_data.get('website'))
