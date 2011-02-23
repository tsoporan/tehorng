from django.db import models
import datetime
from django.contrib.auth.models import User

class Poll(models.Model):

    CHOICES = (
        ('Vote', 'Vote'), 
        ('Feedback', 'Feedback'),
    )

    question = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(help_text="Brief poll description.", blank=True)
    status = models.BooleanField(default=1, help_text="1 is active 0 is closed.")
    type = models.CharField(choices=CHOICES, max_length=255)


    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice

class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    ip = models.CharField(max_length=255, blank=True, null=True, help_text="For anonymous people we'll store their ip's")

    def __unicode__(self):
        return self.choice.choice

class Feedback(models.Model):
    #Generic model for storing some sort of user feedback/suggestions/advice, etc.
    user = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField()
    poll = models.ForeignKey(Poll)
    created = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.body[:30]



