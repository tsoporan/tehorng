# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('blog_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('blog', ['Entry'])


    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('blog_entry')


    models = {
        'blog.entry': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Entry'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['blog']
