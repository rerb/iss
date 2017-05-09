from __future__ import unicode_literals

from django.db import migrations, models
import pycountry


def populate_country_codes(apps, schema_editor):
    Code = apps.get_model("iss", "CountryCode")
    for country in list(pycountry.countries):
        Code.objects.create(country_name=country.name,
                            iso_country_code=country.alpha2)


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0005_membersuite_conversion'),
    ]

    operations = [
        migrations.RunPython(populate_country_codes)
    ]
