from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        IN_PROGRESS = 'in_progress', _('In progress')
        DONE = 'done', _('Answered')
        SPAM = 'spam', _('Spam')

    full_name = models.CharField(_('full name'), max_length=120)
    phone = models.CharField(_('phone number'), max_length=20)
    email = models.EmailField(_('email'), blank=True)
    origin = models.CharField(_('origin'), max_length=120, blank=True)
    destination = models.CharField(_('destination'), max_length=120, blank=True)
    cargo_type = models.CharField(_('cargo type'), max_length=120, blank=True)
    message = models.TextField(_('message'), blank=True)

    language = models.CharField(_('site language'), max_length=5, default='fa')
    status = models.CharField(_('status'), max_length=12, choices=Status.choices, default=Status.NEW, db_index=True)
    staff_note = models.TextField(_('internal note'), blank=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(_('received'), auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('consultation request')
        verbose_name_plural = _('consultation requests')

    def __str__(self):
        return f'{self.full_name} – {self.phone}'
