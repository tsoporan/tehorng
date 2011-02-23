import django.dispatch
from tracking.models import Hit
from django.contrib.contenttypes.models import ContentType

object_hit = django.dispatch.Signal(providing_args=['object', 'request'])

def object_hit_handler(sender, object, request, **kwargs):
    if instance:
        content_type = ContentType.objects.get_for_model(object)
        user = request.user
        object_id = object.id
        action = Action.objects.create(user=user, content_type=content_type, object_id=object_id)
    return


