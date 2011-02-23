from django.db import models
from django.contrib.auth.models import User
import time

class ArtistManager(models.Manager):

    def validate(self):
        """
        Validate invalid artists.
        """
        qs = self.get_query_set().filter(is_valid=False)
        if qs.update(is_valid=True):
             return True
	
	def invalid_artists(self):
		"""
		Return artists that are marked is_valid = False
		"""
		return self.get_query_set().filter(is_valid=False)
	
	def dmca_artists(self):
		"""
		Return artists that are marked dmca.
		"""
		return self.get_query_set().filter(is_dmca=True)
	
	def valid_artists(self):
		"""
		Return artists that are marked is_valid = True
		"""
		return self.get_query_set().filter(is_valid=True)
	
	def no_albums(self):
		"""
		Return valid artists with no albums.	
		"""
		return (artist for artist in self.get_query_set().valid_artists() if artist.albums.exists())

	def has_albums(self):
		"""
		Return valid artists with albums.
		"""
		return (artist for artist in self.get_query_set().valid_artists() if not artist.albums.exists())

	def no_tags(self):
		"""
		Return valid artists with no tags.
		"""
		no_tags = []
		artists = self.valid_artists()
		for artist in artists:
			if not artist.tags.all(): no_tags.append(artist)
		return no_tags

class AlbumManager(models.Manager):

	def invalid_albums(self):
		"""
		Return albums that are marked is_valid = False
		"""
		return self.get_query_set().filter(is_valid=False)
	
	def valid_albums(self):
		"""
		Return albums that are marked is_valid = True
		"""
		return self.get_query_set().filter(is_valid=True)

	def latest_with_links(self):
		"""
		Return latest albums with links.
		"""
		latest = []
		albums = self.valid_albums().order_by('-created').filter()
		for album in albums:
			if album.link_set.all():
				latest.append(album)
		return latest[:10]

	def popular_uploaders(self, number=10):
		"""
		Returns a list of 10 of the most popular album uploaders.
		"""
		d = {}
		albums = self.get_query_set().all()
		for album in albums:
			if album.user:
				d[album.user.username] = album.user.album_set.count()
	
		if number == 0:
			return [album for album in reversed(sorted(d.items(), key=lambda (k,v): (v,k)))]
		return [album for album in reversed(sorted(d.items(), key=lambda (k,v): (v,k)))][:number]

class LinkManager(models.Manager):
	def reported_links(self, number=None):
		"""
		Returns all reported links, by default it returns all which have been reported at least once.
		If "number" is provided, it returns links reported = number.
		"""
		if number:
			return self.get_query_set().filter(reported__exact=number)
		return self.get_query_set().filter(reported__gte=1)


	def popular_uploaders(self, number=10):
		"""
		Returns a list of 10 of the most popular link uploaders.
		"""
		d = {}
		for link in self.get_query_set():
				if d.has_key(link.user.username):
					d[link.user.username] = d[link.user.username]+1
				else:
					d[link.user.username] = 1

		if number == 0:
			return [link for link in sorted(d.items(), key=lambda (k,v): (v,k))]
		return [link for link in sorted(d.items(), key=lambda (k,v): (v,k))]#[:number]

