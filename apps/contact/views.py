from django.shortcuts import render_to_response
from django.template import RequestContext
from contact.forms import ContactForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import mail_admins 
from django.contrib import messages
from django.conf import settings

def contact(request):
    user = request.user
    if request.method == 'POST':
        form = ContactForm(user, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
           
            subject = cd['subject']
            message = cd['message']

            if user.is_authenticated():
                email = user.email
                msg = message + '\n\nFrom: ' + email
                mail_admins(subject, msg)
                messages.success(request, "Your message has been sent! Thanks.")
                return HttpResponseRedirect(reverse('index'))
            else:
                email = cd['email']
                msg = message + '\n\nFrom: ' + email
                mail_admins(subject, msg)
                return HttpResponseRedirect(reverse('contact-success'))
    else:
        form = ContactForm(user)
    
    return render_to_response('contact/contact.html', {
        'form': form,
    }, context_instance=RequestContext(request))

