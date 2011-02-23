"""
A way to represent user activity. Activity should be measured by an action. Currently tehorng is limited to CRUD type functionality.
For example, a user adding an artist would be considerd an action along with editing and deleting.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime
from django.template import mark_safe

HUMAN_FRIENDLY = {
    'add': 'added', 
    'edit': 'edited',
    'delete': 'deleted',
}

class Action(models.Model):
    ACTION_TYPE = (
        ('Add', 'Add'), 
        ('Edit', 'Edit'), 
        ('Remove', 'Remove'), 
    )
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)
    action = models.CharField(max_length=50, choices=ACTION_TYPE) 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    content_object_hard = models.CharField(max_length=255, blank=True)

    def human_msg(self):
        content_object = self.content_object if self.content_object else self.content_object_hard + " (Deleted)"
        return mark_safe(u"%s %s %s:%s" % (self.user.username, HUMAN_FRIENDLY[self.action.lower()], self.content_type.name, content_object))
    
    def __unicode__(self):
        content_object = self.content_object if self.content_object else self.content_object_hard + " (Deleted)"
        return u"%s for %s on %s" % (self.action, self.user.username, content_object)

    def save(self, *args, **kwargs):
        if not self.content_object_hard and self.content_object:
            self.content_object_hard = self.content_object
        super(Action, self).save(*args, **kwargs)
