# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TrackedObject'
        db.create_table('tracking_trackedobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ctype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tracking', ['TrackedObject'])

        # Adding unique constraint on 'TrackedObject', fields ['ctype', 'object_id']
        db.create_unique('tracking_trackedobject', ['ctype_id', 'object_id'])

        # Adding M2M table for field users on 'TrackedObject'
        db.create_table('tracking_trackedobject_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trackedobject', models.ForeignKey(orm['tracking.trackedobject'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('tracking_trackedobject_users', ['trackedobject_id', 'user_id'])

        # Adding model 'TrackedArtist'
        db.create_table('tracking_trackedartist', (
            ('trackedobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tracking.TrackedObject'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tracking', ['TrackedArtist'])

        # Adding model 'TrackedAlbum'
        db.create_table('tracking_trackedalbum', (
            ('trackedobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tracking.TrackedObject'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tracking', ['TrackedAlbum'])

        # Adding model 'TrackedLink'
        db.create_table('tracking_trackedlink', (
            ('trackedobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tracking.TrackedObject'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tracking', ['TrackedLink'])

        # Adding model 'Banned'
        db.create_table('tracking_banned', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tracking', ['Banned'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TrackedObject', fields ['ctype', 'object_id']
        db.delete_unique('tracking_trackedobject', ['ctype_id', 'object_id'])

        # Deleting model 'TrackedObject'
        db.delete_table('tracking_trackedobject')

        # Removing M2M table for field users on 'TrackedObject'
        db.delete_table('tracking_trackedobject_users')

        # Deleting model 'TrackedArtist'
        db.delete_table('tracking_trackedartist')

        # Deleting model 'TrackedAlbum'
        db.delete_table('tracking_trackedalbum')

        # Deleting model 'TrackedLink'
        db.delete_table('tracking_trackedlink')

        # Deleting model 'Banned'
        db.delete_table('tracking_banned')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tracking.banned': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Banned'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'tracking.trackedalbum': {
            'Meta': {'ordering': "('-hits',)", 'object_name': 'TrackedAlbum', '_ormbases': ['tracking.TrackedObject']},
            'trackedobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracking.TrackedObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tracking.trackedartist': {
            'Meta': {'ordering': "('-hits',)", 'object_name': 'TrackedArtist', '_ormbases': ['tracking.TrackedObject']},
            'trackedobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracking.TrackedObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tracking.trackedlink': {
            'Meta': {'ordering': "('-hits',)", 'object_name': 'TrackedLink', '_ormbases': ['tracking.TrackedObject']},
            'trackedobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracking.TrackedObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tracking.trackedobject': {
            'Meta': {'ordering': "('-hits',)", 'unique_together': "(('ctype', 'object_id'),)", 'object_name': 'TrackedObject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['tracking']
