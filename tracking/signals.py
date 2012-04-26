import django.dispatch
from tracking.models import Hit
from django.contrib.contenttypes.models import ContentType

hit = django.dispatch.Signal(providing_args=['object', 'request'])

def hit_handler(sender, object, request, **kwargs):
    content_type = ContentType.objects.get_for_model(object)
    user = None
    if request.user.is_authenticated():
        user = request.user
    
    object_id = object.id
    hit = Hit.objects.create(user=user, content_type=content_type, object_id=object_id)
