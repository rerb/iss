# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0004_organization_primary_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='street',
            new_name='street1',
        ),
        migrations.AddField(
            model_name='organization',
            name='street2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='account_num',
            field=models.TextField(primary_key=True),
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='salesforce_id',
            new_name='membersuite_id',
        ),
        migrations.AlterField(
            model_name='organization',
            name='membersuite_id',
            field=models.IntegerField(blank=True)
        )
    ]
