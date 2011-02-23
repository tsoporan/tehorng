from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import comments
from django.template import RequestContext
from django.contrib import messages
from django.core.mail import send_mail

@login_required
def flag_comment(request, id):
    comment = get_object_or_404(comments.get_model(), pk=id, site__pk=settings.SITE_ID)
    subject = "Comment flagged on tehorng.com!"
    from_email = "Tehorng Staff <staff@tehorng.com>"
    message = """Comment ID: %s\nComment: %s\n\nFlagged on tehorng.com by %s\n""" % (comment.id, comment.comment, request.user) 
    send_mail(subject, message, from_email, ['tsopor@gmail.com',], fail_silently=False)
    messages.success(request, "Comment was flagged successfully")
    return HttpResponseRedirect(comment.content_object.get_absolute_url())

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(comments.get_model(), pk=id, site__pk=settings.SITE_ID)
    
    if comment.user != request.user:
        messages.error(request, "You don't have permission to do that.")
        return HttpResponseRedirect(comment.content_object.get_absolute_url())
    
    if comment.user == request.user:
        comment.is_removed = True
        comment.save()
        messages.success(request, "Comment deleted successfully!")
        return HttpResponseRedirect(comment.content_object.get_absolute_url())
