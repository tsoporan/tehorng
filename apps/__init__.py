from tracking.signals import object_hit
from tracking.signals import object_hit_handler

object_hit.connect(object_hit_handler)
