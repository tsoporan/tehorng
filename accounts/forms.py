from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounts.models import UserProfile
from messaging.models import UserMessage

class RegisterForm(forms.Form):
    username = forms.RegexField(label="Username", regex=r'^\w+$', max_length=35, error_messages={'invalid': "Username must be alphanumeric"})
    email = forms.EmailField(label="E-Mail", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #password1 = forms.CharField(label="Password (again)",widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_exists = User.objects.get(username__iexact=username)
            raise forms.ValidationError('Username already exists.')
        except User.DoesNotExist:
            return username
        return username

    #def clean(self):
        #if 'password' in self.cleaned_data and 'password1' in self.cleaned_data:
        #    if self.cleaned_data['password'] != self.cleaned_data['password1']:
        #        raise forms.ValidationError('Your passwords must match!')
        #    elif len(self.cleaned_data['password']) <= 5:
        #        raise forms.ValidationError('Your password must be greater than 5 characters')
        #return self.cleaned_data

class ChangeEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class ChangeUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ("username",)

class SendPMForm(ModelForm):
    class Meta:
        model = UserMessage
        exclude = ("from_user", "to_user", "read")

class SendMassPMForm(forms.Form):
    to = forms.CharField(label="To", widget=forms.Textarea(attrs={'class': 'to'}), help_text="A comma seperated list of existing user names.")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'msg'}))

    def clean_to(self):
        to = self.cleaned_data['to']
        users = [user.strip() for user in to.split(',') if user]
        error = False
        for user in users:
            if user: #get rid of "" None users.
                try:
                    User.objects.get(username=user)
                except User.DoesNotExist:
                    error = True
        if error:
            raise forms.ValidationError("It appears like one or more of the users don't exist on tehorng! %s" % users)
        return to

class ReportUserForm(forms.Form):
    """
    Form for reporting an user.
    """
    reason = forms.CharField(max_length=255, required=True, help_text='A brief description of the problem.', widget=forms.Textarea)
