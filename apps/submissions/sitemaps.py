from django.contrib.sitemaps import Sitemap
from submissions.models.artist import Artist
from submissions.models.album import Album

class ArtistSitemap(Sitemap):
	changefreq = "never"
	priority = 0.5

	def items(self):
		return Artist.objects.all()
	
	def lastmod(self, obj):
		return obj.modified

class AlbumSitemap(Sitemap):
	changefreq = "never"
	priority = 0.5

	def items(self):
		return Album.objects.all()
	
	def lastmod(self, obj):
		return obj.modified
