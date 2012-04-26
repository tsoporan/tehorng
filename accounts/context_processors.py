from django.contrib.auth.models import User
import datetime
from accounts.models import OnlineUser

def online(request):
    total_online = OnlineUser.objects.onlines().count()
    total_online_users = OnlineUser.objects.online_users().count()
    total_online_guests = total_online - total_online_users
    return {
        'online_users': total_online_users,
        'online_guests': total_online_guests,
    } 
