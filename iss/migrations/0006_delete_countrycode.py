# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0005_membersuite_conversion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CountryCode',
        ),
    ]
