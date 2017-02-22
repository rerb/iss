# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0005_membersuite_conversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='owner',
            field=models.ForeignKey(to='iss.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_defunct',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_member',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
