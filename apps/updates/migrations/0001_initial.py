# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Update'
        db.create_table('updates_update', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
            ('expired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('updates', ['Update'])


    def backwards(self, orm):
        
        # Deleting model 'Update'
        db.delete_table('updates_update')


    models = {
        'updates.update': {
            'Meta': {'object_name': 'Update'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['updates']
