from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.track import Track
from haystack.indexes import *
from haystack import site


class ArtistIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    created = DateTimeField(model_attr='created')
    uploader = CharField(model_attr='uploader', null=True)  

class AlbumIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    created = DateTimeField(model_attr='created')
    uploader = CharField(model_attr='uploader', null=True)  
    
class TrackIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    album = CharField(model_attr="album", null=True)
    artist = CharField(model_attr="album__artist", null=True)
    created = DateTimeField(model_attr='created')

site.register(Artist, ArtistIndex)
site.register(Album, AlbumIndex)
site.register(Track, TrackIndex)
