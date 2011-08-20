from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from accounts.forms import RegisterForm, ChangeEmailForm, ChangeUsernameForm, SendPMForm, SendMassPMForm, ReportUserForm 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import UserProfile
from messaging.models import UserMessage
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic import list_detail
from django.contrib.sites.models import Site
from submissions.models.artist import Artist
from submissions.models.album import Album
from submissions.models.link import Link
from django.views.decorators.cache import cache_page
from recaptcha.client import captcha
from django.utils.safestring import mark_safe
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        if 'recaptcha_challenge_field' in request.POST:
            check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
            if not check_captcha.is_valid:
                messages.error(request, "Captcha was incorrect!") #% check_captcha.error_code)
                return HttpResponseRedirect(reverse('register'))

        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username,email,password = cd['username'], cd['email'], cd['password']   
            
            new_user = User.objects.create_user(username = username, email = email, password = password)  

            #TODO: fix this, weird postgres issue in django 1.3 see trac issue #15682
            user = User.objects.get(username=new_user.username)
            profile = UserProfile.objects.create(user=user)
            
            messages.success(request, "Thanks for registering %s! Welcome to tehorng." % new_user)
            
            authed_user = authenticate(username=username, password=password)
            login(request, authed_user)
            return HttpResponseRedirect(reverse('profile'))    
    else:
        form = RegisterForm(initial=request.POST)
    return render_to_response('registration/register.html', {
        'form': form,
        'captcha': mark_safe(captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)),
    }, context_instance=RequestContext(request))

@login_required
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    artists = profile.artists_for_user(10)
    albums = profile.albums_for_user(10)
    links = profile.links_for_user(10)

    reports = user.report_set.all()

    return render_to_response('accounts/profile.html', {
        'profile': profile,
        'artists_for_user': artists,
        'albums_for_user': albums,
        'links_for_user': links,
        'reports': reports,
    }, context_instance=RequestContext(request))

@login_required
def profile_user(request, username):
    user = get_object_or_404(User, username=username)
    
    if user == request.user:
        return HttpResponseRedirect(reverse('profile'))
    
    profile = UserProfile.objects.get(user=user)
    artists = profile.artists_for_user(10)
    albums = profile.albums_for_user(10)
    links = profile.links_for_user(10)

    return render_to_response('accounts/profile_user.html', {
        'profile': profile,
        'artists_for_user': artists,
        'albums_for_user': albums,
        'links_for_user': links,
    }, context_instance=RequestContext(request))

@login_required
def view_links(request, username=None):
    
    if username:
        user = get_object_or_404(User, username=username)
        links = Link.objects.filter(uploader=user)
    else:
        user = request.user
        links = Link.objects.filter(uploader=user).order_by('-created')
    
    return list_detail.object_list(
        request=request,
        queryset = links,
        paginate_by = 50,
        template_object_name = 'links',
        template_name = 'accounts/viewlinks.html',
        extra_context = {'profile': user.get_profile()}
    )

@login_required
def view_albums(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        albums = Album.objects.filter(uploader=user)
    else:
        user = request.user
        albums = Album.objects.filter(uploader=user).order_by('-created')
    return list_detail.object_list(
        request=request,
        queryset = albums,
        paginate_by = 50,
        template_object_name = 'albums',
        template_name = 'accounts/viewalbums.html',
        extra_context = {'profile': user.get_profile()}
    )

@login_required
def view_artists(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        artists = Artist.objects.filter(uploader=user, is_valid=True)
    else:
        user = request.user
        artists = Artist.objects.filter(uploader=user, is_valid=True).order_by('-created')
    
    return list_detail.object_list(
        request=request,
        queryset = artists,
        paginate_by = 50,
        template_object_name = 'artists',
        template_name = 'accounts/viewartists.html',
        extra_context = {'profile': user.get_profile()}
    )

@login_required
def change_email(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Email changed successfully!")
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ChangeEmailForm(instance=user)
    return render_to_response('accounts/changeemail.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def inbox(request):
    if request.method == 'POST':
        msgids = request.POST.getlist('selected')
        for id in msgids:
            umsg = UserMessage.objects.get(id=id)
            if "delete" in request.POST:
                umsg.delete()
            if "mark" in request.POST:
                umsg.read = True
                umsg.save(email=False)
        messages.success(request, "Action completed successfully!")
        return HttpResponseRedirect(reverse("inbox"))
    return render_to_response('accounts/inbox.html', {}, context_instance=RequestContext(request))

@login_required
def change_username(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Username changed successfully!")
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ChangeUsernameForm(instance=user)
    return render_to_response('accounts/changeusername.html', {
        'form': form,
        'profile': profile,
    }, context_instance=RequestContext(request))

@login_required
def sendpm_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    if request.method == 'POST':
        form = SendPMForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            msg = UserMessage.objects.create(
                to_user = user,
                from_user = request.user,
                message = message,
            )
            messages.success(request, "Message delivered!")
            return HttpResponseRedirect(reverse('profile-user', args=[user.username]))
    else:
        form = SendPMForm()
    return render_to_response('accounts/sendpm.html', {
        'form': form,
        'profile': profile,
    }, context_instance=RequestContext(request))

@login_required
def sendpm(request):
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = SendMassPMForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['to']
            message = form.cleaned_data['message']
            usernames = [username.strip() for username in to.split(',') if username]
            for username in usernames:
                msg = UserMessage.objects.create(
                    to_user = User.objects.get(username=username),
                    from_user = request.user,
                    message = message,
                )
            messages.success(request, "Messages delivered!")
            return HttpResponseRedirect(reverse("profile"))
    else:
        form = SendMassPMForm()
    return render_to_response('accounts/sendmasspm.html', {
        'form': form,
        'profile': profile, 
    }, context_instance=RequestContext(request))

@login_required
def report_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
   
    if request.method == 'POST':
        form = ReportUserForm(request.POST)
        if form.is_valid():
            #do crap
            messages.success(request, "Your report was a success. Admins have been notified.")
            return HttpResponseRedirect(reverse('profile-user', args=[profile.user]))
    else:
        form = ReportUserForm()
    return render_to_response('accounts/reportuser.html', {
        'profile': profile,  
        'form': form,
    }, context_instance=RequestContext(request))
