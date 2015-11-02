# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0002_auto_20151016_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycode',
            name='country_name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='class_profile',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='sector',
            field=models.TextField(blank=True),
        ),
    ]
