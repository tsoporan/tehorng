from django.db import models


class HistoryDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            return HistoryManager(self.model)
        return HistoryManager(self.model, instance)

class HistoryManager(models.Manager):
    def __init__(self, model, instance=None):
        super(HistoryManager, self).__init__()
        self.model = model
        self.instance = instance

    def get_query_set(self):
        if self.instance is None:
            return super(HistoryManager, self).get_query_set()

        filter = {self.instance._meta.pk.name: self.instance.pk}
        return super(HistoryManager, self).get_query_set().filter(**filter)
