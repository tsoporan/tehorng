from tracking.signals import hit, hit_handler

hit.connect(hit_handler)
