from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class UserMessage(models.Model):
    to_user = models.ForeignKey(User, related_name="to_user")
    from_user = models.ForeignKey(User, related_name='from_user')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    read = models.BooleanField(default=False, help_text='Read or unread.')

    class Meta:
        ordering = ("-created",)

    def __unicode__(self):
        return self.message

    def save(self, email=True, *args, **kwargs):
        #sends an email to 'to_user' when message created.
        if email:
            subject = "User has left you a message on tehorng!"
            from_email = "Tehorng Staff <staff@tehorng.com>"
            top = "'%s' has left you a message on tehorng. \n\n" % self.from_user
            body = self.message 
            message = top + body
            send_mail(subject, message, from_email,  [self.to_user.email])
        
        super(UserMessage, self).save(*args, **kwargs)
