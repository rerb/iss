# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('iss_organization', (
            ('account_num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('sf_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('org_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('picklist_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exclude_from_website', self.gf('django.db.models.fields.IntegerField')()),
            ('is_defunct', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_member', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('member_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('business_member_level', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('org_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('carnegie_class', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('class_profile', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('setting', self.gf('django.db.models.fields.CharField')(max_length=33, blank=True)),
            ('longitude', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('latitude', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('street', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('city', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('state', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country_iso', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('website', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sustainability_website', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('enrollment_fte', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stars_participant_status', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pilot_participant', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_signatory', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('iss', ['Organization'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('iss_organization')


    models = {
        'iss.organization': {
            'Meta': {'object_name': 'Organization'},
            'account_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'business_member_level': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'carnegie_class': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'class_profile': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'country': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'country_iso': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'enrollment_fte': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exclude_from_website': ('django.db.models.fields.IntegerField', [], {}),
            'is_defunct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_member': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_signatory': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'longitude': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'member_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'org_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picklist_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pilot_participant': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'setting': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'sf_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stars_participant_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'street': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sustainability_website': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['iss']