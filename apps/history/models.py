import copy
import datetime
from django.contrib.auth.models import User
from django.db import models

import history.manager

class FieldRegistry(object):
    _registry = {}

    def add_field(self, model, field):
        reg = self.__class__._registry.setdefault(model, [])
        reg.append(field)

    def get_fields(self, model):
        return self.__class__._registry.get(model, [])

    def __contains__(self, model):
        return model in self.__class__._registry


class CurrentUserField(models.ForeignKey):
    def __init__(self, **kwargs):
        super(CurrentUserField, self).__init__(User, null=True, **kwargs)

    def contribute_to_class(self, cls, name):
        super(CurrentUserField, self).contribute_to_class(cls, name)
        registry = FieldRegistry()
        registry.add_field(cls, self)

class HistoricalRecords(object):
    
    def contribute_to_class(self, cls, name):
        self.manager_name = name
        models.signals.class_prepared.connect(self.finalize, sender=cls)
    
    def finalize(self, sender, **kwargs):
        history_model = self.create_history_model(sender)

        models.signals.post_save.connect(self.post_save, sender=sender, weak=False)

        models.signals.post_delete.connect(self.post_delete, sender=sender, weak=False)

        descriptor = history.manager.HistoryDescriptor(history_model)
        setattr(sender, self.manager_name, descriptor)

    def post_save(self, instance, created, **kwargs):
        self.create_historical_record(instance, created and '+' or '~')

    def post_delete(self, instance, **kwargs):
        self.create_historical_record(instance, '-')

    def create_historical_record(self, instance, type):
        manager = getattr(instance, self.manager_name)
        attrs = {}
        for field in instance._meta.fields:
            attrs[field.attname] = getattr(instance, field.attname)

        manager.create(history_type=type, **attrs)

    def create_history_model(self, model):

        attrs = self.copy_fields(model)
        attrs.update(self.get_extra_fields(model))
        attrs.update(Meta=type('Meta', (), self.get_meta_options(model)))
        name = 'Historical%s' % model._meta.object_name
        return type(name, (models.Model,), attrs)

    def copy_fields(self, model):
        fields = {'__module__': model.__module__}

        for field in model._meta.fields:
            field = copy.copy(field)

            if isinstance(field, models.AutoField):
                field.__class__ = models.IntegerField

            if field.primary_key or field.unique:
                field.primary_key = False
                field._unique = False
                field.db_index = True

            fields[field.name] = field
        
        return fields

    def get_extra_fields(self, model):

        rel_nm = "_%s_history" % model._meta.object_name.lower()
        return {
            'history_id': models.AutoField(primary_key=True),
            'history_date': models.DateTimeField(default=datetime.datetime.now),
            'history_user': CurrentUserField(related_name=rel_nm),
            'history_type': models.CharField(max_length=1, choices=(
                ('+', 'Created'),
                ('~', 'Changed'),
                ('-', 'Deleted'),
            )),
            'history_object': HistoricalObjectDescriptor(model),
            '__unicode__': lambda self: u'%s as of %s' % (self.history_object,self.history_date)

        }

    def get_meta_options(self, model):
        return {
                'ordering': ('-history_date',),
        }

class HistoricalObjectDescriptor(object):
    def __init__(self,model):
        self.model = model

    def __get__(self, instance, owner):
        values = (getattr(instance, f.attname) for f in self.model._meta.fields)
        return self.model(*values)
