from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ReportManager(models.Manager):
    def reports_for_id(self, ctype, id):
        return self.filter(ctype=ctype, object_id=id)  
    
    def reports_for_ctype(self, ctype):
        return self.filter(ctype=ctype)

class Report(models.Model):
    """A generic reporting model for any object."""
    user = models.ForeignKey(User)
    ctype = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('ctype', 'object_id')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cleared = models.BooleanField(default=False)

    objects = ReportManager()

    class Meta:
        unique_together = ('user', 'ctype', 'object_id',) #user can report object once
        verbose_name = "Reported Item"
        verbose_name_plural = "Reported Items"
    
    def short_reason(self):
        return self.reason[:50]
    
    def __unicode__(self):
        return self.object_id

    def notify(self, user=None, cobj=None):
        #from django.core.mail import send_mail
        from messaging.models import Message

        pass 
