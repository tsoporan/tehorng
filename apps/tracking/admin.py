from django.contrib import admin
from tracking.models import  TrackedArtist, TrackedAlbum, TrackedLink, Banned

class TrackedArtistAdmin(admin.ModelAdmin):
	list_display = ('object', 'ctype',  'object_id', 'hits', 'created')

class TrackedAlbumAdmin(admin.ModelAdmin):
	list_display = ('get_artist', 'object', 'ctype',  'object_id', 'hits', 'created')
	
	def get_artist(self, obj):
		return '%s' % (obj.object.artist)
	get_artist.short_description = 'Artist'

class TrackedLinkAdmin(admin.ModelAdmin):
	list_display = ('get_artist', 'get_album', 'object', 'ctype',  'object_id', 'hits', 'created')
	
	def get_artist(self, obj):
		return '%s' % (obj.object.album.artist)
	get_artist.short_description = 'Artist'

	def get_album(self, obj):
		return '%s' % (obj.object.album)
	get_album.short_description = 'Album'

class BannedAdmin(admin.ModelAdmin):
	pass


admin.site.register(TrackedArtist, TrackedArtistAdmin)
admin.site.register(TrackedAlbum, TrackedAlbumAdmin)
admin.site.register(TrackedLink, TrackedLinkAdmin)
admin.site.register(Banned, BannedAdmin)
