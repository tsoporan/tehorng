from messaging.models import UserMessage
from django.contrib.auth.models import User
import datetime

def user_messages(request):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=request.user)
            profile = user.get_profile()
            messages = profile.get_user_messages()
            unread = messages.filter(read=False)
            return {'user_messages': messages, 'unread': unread}
        except:
            pass
    return {}

