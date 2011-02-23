from activity.models import Action
import django.dispatch
from django.contrib.contenttypes.models import ContentType

add_object = django.dispatch.Signal(providing_args=['instance', 'action'])
edit_object = django.dispatch.Signal(providing_args=['instance', 'action'])
delete_object = django.dispatch.Signal(providing_args=['instance', 'action'])
#action = django.dispatch.Signal(providing_args=['instance', 'action'])

def action_handler(sender, instance, action, **kwargs):
    if instance and action:
        content_type = ContentType.objects.get_for_model(instance) 
        user = instance.uploader
        object_id = instance.id
        action = Action.objects.create(user=user, action=action, content_type=content_type, object_id=object_id)
    return

