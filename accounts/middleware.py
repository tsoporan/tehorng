from accounts.models import OnlineUser

class OnlineUserMiddleware(object):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated():
            o, created = OnlineUser.objects.get_or_create(user=user)
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            o, created = OnlineUser.objects.get_or_create(ident=ip)
        if not created:
            o.save()
