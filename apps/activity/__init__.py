from activity.signals import add_object, edit_object, delete_object
from activity.signals import action_handler

add_object.connect(action_handler)
edit_object.connect(action_handler)
delete_object.connect(action_handler)
