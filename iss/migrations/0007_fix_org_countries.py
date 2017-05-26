# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pycountry


def fix_countries(apps, schema_editor):
    Organization = apps.get_model("iss", "Organization")
    for org in Organization.objects.all():
        if org.country_iso:
            try:
                pyc = pycountry.countries.get(alpha_2=org.country_iso)
            except KeyError:
                return

            org.country = pyc.name
            org.save()


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0006_delete_countrycode'),
    ]

    operations = [
        migrations.RunPython(fix_countries)
    ]
