from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime

class TrackedManager(models.Manager):
    def total_hits(self):
        hits = self.get_query_set().values('hits')
        return sum([obj['hits'] for obj in hits])


class Hit(models.Model):
    user = models.ForeignKey(User, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"%s hit on %s:%s" % (self.user or "Anonymous", self.content_type, self.content_object)

class TrackedObject(models.Model):
    """
    A tracked object is incrememnted when it is "used".
    Example: /track/link/232/ creates a new tracked object tying it
    to the request user the object content type, object_id and increases 
    the hit counter.
    """
    users = models.ManyToManyField(User) #many users can hit one object / hit object can have many users
    ctype = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=255)
    object = generic.GenericForeignKey('ctype', 'object_id')
    hits = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-hits',)
        get_latest_by = "created"
        unique_together = (('ctype', 'object_id'))

class TrackedArtist(TrackedObject):
    """Inherits from TrackedObj but allows for seperation."""
    def __unicode__(self):
        return self.object.name

class TrackedAlbum(TrackedObject):
    """Inherits from TrackedObj but allows for seperation."""
    def __unicode__(self):
        return self.object.name

class TrackedLink(TrackedObject):
    """Inherits from TrackedObj but allows for seperation."""
    objects = TrackedManager()
    def __unicode__(self):
        return self.object.album.name

#No better place to put this, it is technically part of "tracking".
class Banned(models.Model):
    """
    A singular IP Address that will be banned.
    """
    ip_addr = models.IPAddressField('IP Address', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Banned'
        verbose_name_plural = 'Banned'

    def __unicode__(self):
        if self.ip_addr and not self.user:
            return self.ip_addr
        elif self.user and not self.ip_addr:
            return self.user.username
        else:
            return '%s : %s' % (self.user.username, self.ip_addr)

    
