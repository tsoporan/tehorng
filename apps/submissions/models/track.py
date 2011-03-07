from django.db import models
from submissions.models.utils import strip_punc
from django.contrib.auth.models import User
from submissions.models.album import Album
from django.contrib.contenttypes.models import ContentType

class Track(models.Model):
    """
    A single track(song) for an album.
    """
    URL_CHOICES =  (
        ('download', 'download'),
        ('stream','stream'),
        ('buy','buy'),
    )
    
    title = models.CharField(max_length=255)
    cleaned_name = models.CharField(max_length=255, blank=True, null=True, editable=False, help_text="A cleaned name without punctuation or weird stuff.")
    track_number = models.IntegerField(blank=True, null=True)
    #Replace by regexfield r'[0-9:]+' in forms
    duration = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField('URL', blank=True, null=True)
    url_type = models.CharField('Type', max_length=255, choices=URL_CHOICES, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, blank=True, null=True, help_text="The uploader of this track.")
    album = models.ForeignKey(Album, related_name="tracks", help_text="The album to which this track belongs.")
    mbid = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        app_label = "submissions"
        ordering = ('track_number', 'title')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('album-detail', (), {'artist': self.album.artist.slug, 'album': self.album.slug })

    def save(self, *args, **kwargs):
        if not self.cleaned_name:
            self.cleaned_name = strip_punc(self.title)   
        super(Track, self).save(*args, **kwargs)

