# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0006_auto_20170222_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_directory_opt_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='membership',
            name='receives_membership_benefits',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_defunct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_member',
            field=models.BooleanField(default=False),
        ),
    ]
