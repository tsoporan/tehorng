from django.db import models
from submissions.models.utils import gen_hash
from submissions.managers import LinkManager
from django.contrib.auth.models import User
from submissions.models.album import Album
from tracking.models import TrackedLink
from django.contrib.contenttypes.models import ContentType
import datetime

class Link(models.Model):
    """
    A single link that is unique for an album.
    """
    URL_TYPES = (
        ('download', 'download'),
        ('stream', 'stream'),
        ('buy', 'buy'),
    )

    BITRATE_CHOICES =  (
        ('128K','128K'),
        ('192K','192K'),
        ('256K','256K'),
        ('320K','320K'),
        ('lossless','Lossless'),
        ('V0', 'V0'),
        ('V1', 'V1'),
        ('V2', 'V2'),
        ('other', 'Other'),
    )

    FORMAT_CHOICES =  (
        ('mp3','MP3'),
        ('aac','AAC'),
        ('flac','FLAC'),
        ('ogg','OGG'),
        ('other', 'Other'),
    )

    url = models.URLField('URL')
    url_type = models.CharField('Type', max_length=30, choices=URL_TYPES, blank=False)
    bitrate = models.CharField(max_length=255, choices=BITRATE_CHOICES, blank=True)
    format = models.CharField(max_length=255, choices=FORMAT_CHOICES, blank=True)
    uploader = models.ForeignKey(User, help_text="The uploader of this link.")
    album = models.ForeignKey(Album, related_name="links", help_text="The album to which this link belongs.")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=255, blank=True)
    part = models.IntegerField(default=1, blank=True, null=True, help_text="This field is used for related links to signify a link part.")
    
    last_edit = models.CharField(max_length=255, editable=False, blank=True, null=True, help_text="Last editor of this link.")
    objects = LinkManager()

    expires = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=30), help_text="Link will be checked for expiration every 30 days.")
    dead = models.BooleanField(default=0, help_text="This link is probably dead.")


    class Meta:
        ordering = ('url_type', 'bitrate')
        unique_together = ('album', 'url') #url unique per album
        verbose_name = "Link"
        verbose_name_plural = "Links"
        app_label = "submissions"

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = gen_hash(self.id)   
        super(Link, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    def delete(self, *args, **kwargs):
        """On delete we need to make sure we get rid of the Tracked object or else we'll have None objects in our database."""
        try:
            tracked = TrackedLink.objects.get(ctype=ContentType.objects.get(name='link'), object_id=self.id)
            tracked.delete()
        except TrackedLink.DoesNotExist:
            pass # doesn't exist
        super(Link, self).delete(*args, **kwargs)


