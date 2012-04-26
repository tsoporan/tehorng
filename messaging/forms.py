from django import forms
from django.forms import ModelForm
from messaging.models import UserMessage

class SendMessage(ModelForm):
	to_user = forms.CharField(require=True)
	class Meta:
		model = UserMessage
		exclude = ('from_user', 'read')
