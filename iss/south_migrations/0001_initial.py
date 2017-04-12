# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CountryCode'
        db.create_table('iss_countrycode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('iso_country_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal('iss', ['CountryCode'])

        # Adding model 'OrganizationType'
        db.create_table('iss_organizationtype', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('iss', ['OrganizationType'])

        # Adding model 'Organization'
        db.create_table('iss_organization', (
            ('account_num', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('salesforce_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('membersuite_account_num', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('membersuite_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('org_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('picklist_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('exclude_from_website', self.gf('django.db.models.fields.IntegerField')()),
            ('is_defunct', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_member', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('member_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('business_member_level', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('org_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iss.OrganizationType'], null=True)),
            ('carnegie_class', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('class_profile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('setting', self.gf('django.db.models.fields.CharField')(max_length=33, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('street1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('street2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('country_iso', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sustainability_website', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('enrollment_fte', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stars_participant_status', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pilot_participant', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_signatory', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('primary_email', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('iss', ['Organization'])

        # Adding model 'MembershipProduct'
        db.create_table('iss_membershipproduct', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('iss', ['MembershipProduct'])

        # Adding model 'Membership'
        db.create_table('iss_membership', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iss.Organization'], null=True)),
            ('membership_directory_opt_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receives_membership_benefits', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('current_dues_amount', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iss.MembershipProduct'])),
            ('last_modified_date', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('join_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('termination_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('renewal_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('iss', ['Membership'])


    def backwards(self, orm):
        # Deleting model 'CountryCode'
        db.delete_table('iss_countrycode')

        # Deleting model 'OrganizationType'
        db.delete_table('iss_organizationtype')

        # Deleting model 'Organization'
        db.delete_table('iss_organization')

        # Deleting model 'MembershipProduct'
        db.delete_table('iss_membershipproduct')

        # Deleting model 'Membership'
        db.delete_table('iss_membership')


    models = {
        'iss.countrycode': {
            'Meta': {'object_name': 'CountryCode'},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_country_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        'iss.membership': {
            'Meta': {'object_name': 'Membership'},
            'current_dues_amount': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified_date': ('django.db.models.fields.DateField', [], {}),
            'membership_directory_opt_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iss.Organization']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iss.MembershipProduct']"}),
            'receives_membership_benefits': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'renewal_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'termination_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'iss.membershipproduct': {
            'Meta': {'object_name': 'MembershipProduct'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'iss.organization': {
            'Meta': {'object_name': 'Organization'},
            'account_num': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'business_member_level': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'carnegie_class': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'class_profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country_iso': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'enrollment_fte': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exclude_from_website': ('django.db.models.fields.IntegerField', [], {}),
            'is_defunct': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_member': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_signatory': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'member_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'membersuite_account_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'membersuite_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'org_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iss.OrganizationType']", 'null': 'True'}),
            'picklist_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pilot_participant': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'primary_email': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'salesforce_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'setting': ('django.db.models.fields.CharField', [], {'max_length': '33', 'null': 'True', 'blank': 'True'}),
            'stars_participant_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'street1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'street2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sustainability_website': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'iss.organizationtype': {
            'Meta': {'object_name': 'OrganizationType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['iss']