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

class Action(models.Model):
    ACTION_TYPE = (
        ('Add', 'added'), 
        ('Edit', 'edited'), 
        ('Delete', 'deleted'), 
        ('Add Resource', 'added resource'),
        ('Add Image', 'added image'), 
    )
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)
    action = models.CharField(max_length=50, choices=ACTION_TYPE) 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def human_msg(self):
        return mark_safe(u"%s %s %s:%s" % (self.user.username, self.get_action_display(), self.content_type.name, self.content_object))
    
    def __unicode__(self):
        return u"%s for %s on %s" % (self.get_action_display(), self.user.username, self.content_object)
