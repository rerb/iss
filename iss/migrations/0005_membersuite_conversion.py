# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0004_organization_primary_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipProduct',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False,
                                        primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False,
                                        primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('membership_directory_opt_out', models.BooleanField(default=False)),
                ('receives_membership_benefits', models.BooleanField(default=True)),
                ('current_dues_amount', models.CharField(max_length=255, null=True, blank=True)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('type', models.CharField(max_length=255)),
                ('last_modified_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('join_date', models.DateField(null=True, blank=True)),
                ('termination_date', models.DateField(null=True, blank=True)),
                ('renewal_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Domain',
        ),
        migrations.DeleteModel(
            name='DomainToOrg',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='street',
        ),
        migrations.AddField(
            model_name='organization',
            name='membersuite_account_num',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='membersuite_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='street1',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='street2',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='account_num',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='business_member_level',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='carnegie_class',
            field=models.TextField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='class_profile',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country_iso',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_defunct',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_member',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='organization',
            name='latitude',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='longitude',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='member_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='organization',
            name='org_type',
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(to='iss.OrganizationType', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='picklist_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='postal_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='primary_email',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='salesforce_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='sector',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='setting',
            field=models.CharField(max_length=33, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stars_participant_status',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='state',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='sustainability_website',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='owner',
            field=models.ForeignKey(to='iss.Organization', null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='product',
            field=models.ForeignKey(to='iss.MembershipProduct'),
        ),
    ]
