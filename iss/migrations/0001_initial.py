# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_name', models.CharField(unique=True, max_length=256)),
                ('iso_country_code', models.CharField(unique=True, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024)),
                ('account_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DomainToOrg',
            fields=[
                ('domain_id', models.IntegerField(serialize=False, primary_key=True)),
                ('org_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('account_num', models.IntegerField(serialize=False, primary_key=True)),
                ('salesforce_id', models.TextField(blank=True)),
                ('org_name', models.TextField(blank=True)),
                ('picklist_name', models.CharField(max_length=255, blank=True)),
                ('exclude_from_website', models.IntegerField()),
                ('is_defunct', models.IntegerField(null=True, blank=True)),
                ('is_member', models.IntegerField(null=True, blank=True)),
                ('member_type', models.CharField(max_length=255, blank=True)),
                ('business_member_level', models.CharField(max_length=255, blank=True)),
                ('sector', models.CharField(max_length=765, blank=True)),
                ('org_type', models.TextField(blank=True)),
                ('carnegie_class', models.TextField(max_length=255, blank=True)),
                ('class_profile', models.CharField(max_length=765, blank=True)),
                ('setting', models.CharField(max_length=33, blank=True)),
                ('longitude', models.TextField(blank=True)),
                ('latitude', models.TextField(blank=True)),
                ('street', models.TextField(blank=True)),
                ('city', models.TextField(blank=True)),
                ('state', models.TextField(blank=True)),
                ('postal_code', models.CharField(max_length=255, blank=True)),
                ('country', models.TextField(blank=True)),
                ('country_iso', models.CharField(max_length=3, blank=True)),
                ('website', models.TextField(blank=True)),
                ('sustainability_website', models.TextField(blank=True)),
                ('enrollment_fte', models.IntegerField(null=True, blank=True)),
                ('stars_participant_status', models.CharField(max_length=255, blank=True)),
                ('pilot_participant', models.IntegerField(null=True, blank=True)),
                ('is_signatory', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
