from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if not user.is_authenticated():
            self.fields['email'] = forms.EmailField(required=True)



