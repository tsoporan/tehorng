# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Artist'
        db.create_table('submissions_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('cleaned_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_dmca', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('last_edit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('formed', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_touring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tags', self.gf('tagging.fields.TagField')(blank=False)),
            ('mbid_tracks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lastfm_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submissions', ['Artist'])

        # Adding model 'ArtistResource'
        db.create_table('submissions_artistresource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['submissions.Artist'])),
        ))
        db.send_create_signal('submissions', ['ArtistResource'])

        # Adding unique constraint on 'ArtistResource', fields ['artist', 'url']
        db.create_unique('submissions_artistresource', ['artist_id', 'url'])

        # Adding model 'Album'
        db.create_table('submissions_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cleaned_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('last_edit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='albums', to=orm['submissions.Artist'])),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tags', self.gf('tagging.fields.TagField')(blank=False)),
            ('mbid_tracks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lastfm_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submissions', ['Album'])

        # Adding unique constraint on 'Album', fields ['artist', 'slug']
        db.create_unique('submissions_album', ['artist_id', 'slug'])

        # Adding model 'AlbumResource'
        db.create_table('submissions_albumresource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['submissions.Album'])),
        ))
        db.send_create_signal('submissions', ['AlbumResource'])

        # Adding unique constraint on 'AlbumResource', fields ['album', 'url']
        db.create_unique('submissions_albumresource', ['album_id', 'url'])

        # Adding model 'Link'
        db.create_table('submissions_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('bitrate', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['submissions.Album'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('part', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('last_edit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 20, 23, 34, 43, 807805))),
            ('dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submissions', ['Link'])

        # Adding unique constraint on 'Link', fields ['album', 'url']
        db.create_unique('submissions_link', ['album_id', 'url'])

        # Adding model 'Track'
        db.create_table('submissions_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cleaned_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('track_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('url_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['submissions.Album'])),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('submissions', ['Track'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Link', fields ['album', 'url']
        db.delete_unique('submissions_link', ['album_id', 'url'])

        # Removing unique constraint on 'AlbumResource', fields ['album', 'url']
        db.delete_unique('submissions_albumresource', ['album_id', 'url'])

        # Removing unique constraint on 'Album', fields ['artist', 'slug']
        db.delete_unique('submissions_album', ['artist_id', 'slug'])

        # Removing unique constraint on 'ArtistResource', fields ['artist', 'url']
        db.delete_unique('submissions_artistresource', ['artist_id', 'url'])

        # Deleting model 'Artist'
        db.delete_table('submissions_artist')

        # Deleting model 'ArtistResource'
        db.delete_table('submissions_artistresource')

        # Deleting model 'Album'
        db.delete_table('submissions_album')

        # Deleting model 'AlbumResource'
        db.delete_table('submissions_albumresource')

        # Deleting model 'Link'
        db.delete_table('submissions_link')

        # Deleting model 'Track'
        db.delete_table('submissions_track')


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
        'submissions.album': {
            'Meta': {'ordering': "('name', '-created')", 'unique_together': "(('artist', 'slug'),)", 'object_name': 'Album'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'albums'", 'to': "orm['submissions.Artist']"}),
            'cleaned_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_edit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'lastfm_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mbid_tracks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'blank': 'False'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'submissions.albumresource': {
            'Meta': {'unique_together': "(('album', 'url'),)", 'object_name': 'AlbumResource'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['submissions.Album']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'submissions.artist': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Artist'},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cleaned_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'formed': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_dmca': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_touring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_edit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'lastfm_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mbid_tracks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'blank': 'False'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'submissions.artistresource': {
            'Meta': {'unique_together': "(('artist', 'url'),)", 'object_name': 'ArtistResource'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': "orm['submissions.Artist']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'submissions.link': {
            'Meta': {'ordering': "('url_type', 'bitrate')", 'unique_together': "(('album', 'url'),)", 'object_name': 'Link'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['submissions.Album']"}),
            'bitrate': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 20, 23, 34, 43, 807805)'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'part': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'submissions.track': {
            'Meta': {'ordering': "('track_number', 'title')", 'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': "orm['submissions.Album']"}),
            'cleaned_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['submissions']
