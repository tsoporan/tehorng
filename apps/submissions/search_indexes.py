import datetime
from haystack import indexes
from haystack import site
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link 
from submissions.models.track import Track

class ArtistIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    uploader = indexes.CharField(model_attr='uploader', null=True)  

class AlbumIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    uploader = indexes.CharField(model_attr='uploader', null=True)  
    
class TrackIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    album = indexes.CharField(model_attr="album", null=True)
    artist = indexes.CharField(model_attr="album__artist", null=True)
    created = indexes.DateTimeField(model_attr='created')

site.register(Artist, ArtistIndex)
site.register(Album, AlbumIndex)
site.register(Track, TrackIndex)
