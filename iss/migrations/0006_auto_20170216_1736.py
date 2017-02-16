# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0005_membersuite_conversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('membership_directory_opt_out', models.BooleanField()),
                ('receives_membership_benefits', models.BooleanField()),
                ('current_dues_amount', models.CharField(max_length=255)),
                ('expiration_date', models.DateField()),
                ('type', models.CharField(max_length=255)),
                ('last_modified_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('join_date', models.DateField()),
                ('termination_date', models.DateField()),
                ('renewal_date', models.DateField()),
                ('owner', models.ForeignKey(to='iss.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipProduct',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='product',
            field=models.ForeignKey(to='iss.MembershipProduct'),
        ),
    ]
