from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from submissions.models.artist import Artist, ArtistResource 
from submissions.models.album import Album, AlbumResource
from submissions.models.link import Link
from submissions.models.track import Track

from reversion.admin import VersionAdmin

from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment 

class MyCommentsAdmin(CommentsAdmin):
    list_display = ('name', 'content_type','content_object', 'submit_date', 'comment', 'is_public', 'is_removed')

admin.site.unregister(Comment)
admin.site.register(Comment, MyCommentsAdmin)

def make_active(modeladmin, request, queryset):
    queryset.update(is_valid=True)
make_active.short_description = "Set to active."

class ArtistResourceInline(admin.TabularInline):
    raw_id_fields = ('uploader',)
    model = ArtistResource
    extra = 3

class AlbumResourceInline(admin.TabularInline):
    raw_id_fields = ('uploader',)
    model = AlbumResource
    extra = 3

class TrackInline(admin.TabularInline):
    raw_id_fields = ('uploader',)
    model = Track
    extra = 3

class ArtistAdmin(VersionAdmin):
    list_display = ('name', 'slug','cleaned_name', 'id', 'is_valid', 'is_dmca', 'uploader', 'created', 'modified')
    search_fields = ('name',)
    date_hierarchy = 'created'
    list_filter = ('is_valid', 'is_dmca', 'is_public')
    inlines = [ArtistResourceInline,]
    raw_id_fields = ('uploader',)

    actions = [make_active]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'is_valid', 'is_dmca', 'is_public', 'uploader' ),
        }),
        ('Artist Information', {
            'fields': ('origin', 'formed', 'members', 'biography', 'is_touring', 'mbid', 'tags'),
        }),
    )

class AlbumAdmin(VersionAdmin):
    list_display = ('name', 'slug','cleaned_name', 'id', 'artist', 'uploader', 'created', 'modified')
    list_filter = ('is_valid', 'is_public')
    search_fields = ('name',)
    date_hierarchy = 'created'
    raw_id_fields = ('uploader',)

    inlines = [AlbumResourceInline, TrackInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'is_valid', 'is_public', 'uploader','artist'),
        }),
        ('Album Information', {
            'fields': ('release_date', 'mbid', 'tags'),
        }),
    )


class LinkAdmin(VersionAdmin):
    list_display = ('url', 'album', 'get_artist', 'uploader', 'created', 'modified')
    search_fields = ('url', 'bitrate', 'format', 'uploader__username',)
    date_hierarchy = 'created'
    raw_id_fields = ('uploader', 'album')
    
    def get_artist(self, obj):
        return '%s' % (obj.album.artist)
    get_artist.short_description = 'Artist'

class ArtistResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'artist', 'uploader', 'created',)
    raw_id_fields = ('uploader', 'artist')

class AlbumResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'album', 'uploader', 'created',)
    raw_id_fields = ('uploader', 'album')

class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'track_number', 'duration', 'uploader', 'created', 'modified')
    raw_id_fields = ('uploader', 'album')


admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistResource, ArtistResourceAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumResource, AlbumResourceAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Link, LinkAdmin)
