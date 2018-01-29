from django.contrib import admin
from .models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    fields = ('account_num', 'org_name', 'city', 'state', 'country_iso')
admin.site.register(Organization, OrganizationAdmin)
