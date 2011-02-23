from polls.models import Feedback
from django.forms import ModelForm
from django import forms

class FeedbackForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': '10', 'cols': '50', }))

    class Meta:
        model = Feedback
        exclude = ('created', 'user', 'poll')
