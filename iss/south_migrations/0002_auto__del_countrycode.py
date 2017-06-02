# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CountryCode'
        db.delete_table('iss_countrycode')


    def backwards(self, orm):
        # Adding model 'CountryCode'
        db.create_table('iss_countrycode', (
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('iso_country_code', self.gf('django.db.models.fields.CharField')(max_length=2, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('iss', ['CountryCode'])


    models = {
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