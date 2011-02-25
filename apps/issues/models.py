from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

STATUS_CHOICES = (
    (1, 'Open'),
    (2, 'Working'),
    (3, 'Closed'),
    (4, 'Pending'),
    (5, 'Reopened'),
    (6, 'Complete'),
)

PRIORITY_CHOICES = (
    (1, 'Very High'),
    (2, 'High'),
    (3, 'Moderate'),
    (4, 'Low'), 
    (5, 'Very Low'),
    (6, 'N/A'),
)

ISSUE_TYPES = (
    (1, 'Enhancement'),
    (2, 'Defect'),
)

class Issue(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    submitter = models.ForeignKey(User)
    type = models.IntegerField(choices=ISSUE_TYPES)
    description = models.TextField(blank=True)
    status = models.IntegerField(default=4, choices=STATUS_CHOICES)
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)

    class Meta:
        ordering = ['status', 'priority', 'pub_date', 'title']

    def __unicode__(self):
        return self.title

    def html_class(self):
        if self.priority == 1:
            return "vhigh"
        elif self.priority == 2:
            return "high"
        elif self.priority == 3:
            return "mod"
        elif self.priority == 4:
            return "low"
        else:
            return "vlow"
    
    @property
    def is_complete(self):
        if self.status == 6: return True

    @property
    def is_reopened(self):
        if self.status == 5: return True   
