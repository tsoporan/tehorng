from django import template
from activity.models import Action
from django.contrib.contenttypes.models import ContentType

register = template.Library()

def get_recent_activity(parser, token):
    try:
        tag_name, obj, _as, var = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%s tag requires arguments" % token.contents.split()[0])

    return ActivityNode(obj, var)

class ActivityNode(template.Node):
    def __init__(self, obj, var):
        self.obj = template.Variable(obj)
        self.var = var

    def render(self, context):
        actual_object = self.obj.resolve(context)
        try:
            context[self.var] = Action.objects.filter(object_id=actual_object.id, content_type=ContentType.objects.get_for_model(actual_object))
        except:
            pass

        return ''

register.tag('get_recent_activity', get_recent_activity)
