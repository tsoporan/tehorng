from django.contrib.comments.signals import comment_was_posted
from django.core.mail import send_mail
from messaging.models import UserMessage
from submissions.models.link import Link
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

#def on_linkSave(sender, instance, **kwargs):
#    if os.path.exists('/tmp/superbot.pid'):
#        f = open('/tmp/tehorngdata', 'w')
#        out = "[{C9}tehorng link{}] {C7}%s - %s{} <{LINK}%s{}> [{C10} %s/{C5} %s/{C6} %s{}]" % (instance.album.artist, instance.album, instance.url, instance.bitrate, instance.format, instance.url_type)
#        f.write(out)
#        f.close()
#        pid = open('/tmp/superbot.pid', 'r').read()
#        os.system("kill -s USR1 %s" % pid)  
#post_save.connect(on_linkSave, sender=Link)

def commentOnObject(sender, comment, request, **kwargs):
    commenter = comment.user
    try:
        uploader = comment.content_object.uploader
    except AttributeError: #comments don't have uploaders
        uploader = User.objects.get(username=comment.content_object.author)

    from_email = "tehorng <staff@tehorng.com>"
    subject = "User comment on an %s you've uploaded!" % comment.content_type  
    message = """%s commented on %s and said: \n\n%s""" % (comment.user, comment.content_object, comment.comment)
    to_email = uploader.email #the objects uploader's email
    
    #should only send if the person is OTHER then the uploader
    #we do not want to send emails or create user messages for the uploader also
    
    if commenter != uploader:
    
        send_mail(subject, message, from_email, [to_email], fail_silently=True) #fail silently we don't want to cause errors if this doesn't work

        message = UserMessage(
            to_user = uploader,
            from_user = commenter,
            message = message,
        )
        message.save(email=False) #don't email we email above

comment_was_posted.connect(commentOnObject)
