from django.db import models
from django.contrib.auth.models import User, Group
from messaging.models import UserMessage
from datetime import datetime, timedelta
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from django.utils.hashcompat import sha_constructor

LAST_ONLINE_DURATION = 600 #10 minutes

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    warning = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __unicode__(self):
        return self.user.username 

    def get_user_messages(self):
        messages = UserMessage.objects.filter(to_user__exact=self.user)
        return messages

    def links_for_user(self, number=None):
        """Return all links for this user. """
        if not number:
            return Link.objects.filter(uploader=self.user).order_by('-created')
        else:
            return Link.objects.filter(uploader=self.user).order_by('-created')[:number]

    def albums_for_user(self, number=None):
        """Return all albums for this user. """
        if not number:
            return Album.objects.filter(uploader=self.user).order_by('-created')
        else:
            return Album.objects.filter(uploader=self.user).order_by('-created')[:number]

    def artists_for_user(self, number=None):
        """Return all artists for this user. """
        if not number:
            return Artist.objects.filter(uploader=self.user, is_valid=True).order_by('-created')
        else:
            return Artist.objects.filter(uploader=self.user, is_valid=True).order_by('-created')[:number]
    
    def reports_for_user(self):
        """Return all reported objects for this user. """
        return self.user.report_set.all()

class OnlineManager(models.Manager):
    def onlines(self):
        now = datetime.now()
        return OnlineUser.objects.filter(updated__gte = now - timedelta(seconds=LAST_ONLINE_DURATION))

    def online_users(self):
        return self.onlines().filter(user__isnull=False)

class OnlineUser(models.Model):
    user = models.OneToOneField(User, related_name="online", blank=True, null=True)
    ident = models.CharField(max_length=200, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OnlineManager()

    def __unicode__(self):
        return self.ident

    def username(self):
        return self.ident.split(' ')[0]

    def user_id(self):
        ident = self.ident.split(' ')
        if len(ident) > 2:
            return ident[1]
        return ''

    def online(self):
        now = datetime.now()
        if (now - self.updated).seconds < LAST_ONLINE_DURATION:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.user:
            self.ident = '%s %s' % (self.user.username, self.user.pk)
        super(OnlineUser, self).save(*args, **kwargs)
