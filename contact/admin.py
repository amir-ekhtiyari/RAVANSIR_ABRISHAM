from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'route_display', 'cargo_type', 'status', 'language', 'created_at')
    list_filter = ('status', 'language', 'created_at')
    list_editable = ('status',)
    search_fields = ('full_name', 'phone', 'email', 'origin', 'destination', 'cargo_type', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('full_name', 'phone', 'email', 'origin', 'destination', 'cargo_type', 'message',
                       'language', 'ip_address', 'user_agent', 'created_at')
    fieldsets = (
        (_('Request'), {'fields': ('full_name', 'phone', 'email', 'origin', 'destination', 'cargo_type', 'message')}),
        (_('Follow-up'), {'fields': ('status', 'staff_note')}),
        (_('Technical'), {'classes': ('collapse',), 'fields': ('language', 'ip_address', 'user_agent', 'created_at')}),
    )

    @admin.display(description=_('route'))
    def route_display(self, obj):
        return ' → '.join(part for part in (obj.origin, obj.destination) if part) or '—'

    def has_add_permission(self, request):
        return False
