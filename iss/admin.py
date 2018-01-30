from django.contrib import admin
from .models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('account_num', 'org_name', 'city', 'state', 'country_iso')
    search_fields = ('org_name', 'account_num')
admin.site.register(Organization, OrganizationAdmin)
