from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import CompanyInfo

admin.site.site_header = _('Ravan Seir Abrisham – website management')
admin.site.site_title = _('Ravan Seir Abrisham')
admin.site.index_title = _('Website content')


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Name'), {'fields': ('name_fa', 'name_en', 'name_tr', 'short_name_fa', 'short_name_en', 'short_name_tr',
                                'tagline_fa', 'tagline_en', 'tagline_tr')}),
        (_('Texts'), {'fields': ('short_description_fa', 'short_description_en', 'short_description_tr',
                                 'description_fa', 'description_en', 'description_tr')}),
        (_('Contact details'), {'fields': ('email', 'office_phone', 'mobile', 'work_phone',
                                           'address_fa', 'address_en', 'address_tr')}),
        (_('Marand branch'), {'fields': ('branch_address_fa', 'branch_address_en', 'branch_address_tr', 'branch_phone')}),
        (_('Images'), {'fields': ('logo', 'hero_image', 'about_image')}),
    )

    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = CompanyInfo.objects.first()
        if obj:
            return redirect(reverse('admin:core_companyinfo_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)
