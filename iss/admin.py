from django.contrib import admin
from .models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('membersuite_id', 'account_num', 'org_name', 'city',
        'state', 'country_iso')
    search_fields = ('org_name', '=membersuite_id')
admin.site.register(Organization, OrganizationAdmin)
