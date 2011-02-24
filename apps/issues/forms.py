from django import forms
from django.forms.fields import IntegerField
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.contrib.auth.models import User

from issues.models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description')


class IssueEditForm(forms.ModelForm):
    #Edit forms will only be available to admins right now, therefore displaying all fields.
    class Meta:
        model = Issue
    
