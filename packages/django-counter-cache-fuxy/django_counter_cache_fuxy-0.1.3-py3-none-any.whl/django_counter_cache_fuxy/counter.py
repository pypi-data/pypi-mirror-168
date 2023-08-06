from django.db.models import F
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save

from .fields import CounterCacheField

counters = {}


class Counter(object):
    """
    Counter keeps the CounterCacheField counter named *counter_name* up to
    date. Whenever changes are made to instances of the counted child
    model, i.e. the model that defines the foreign field
    *foreign_field*, the counter is potentially incremented/decremented.
    A optional callback function *is_in_counter* can be supplied for
    control over exactly which child model instances are to be counted.
    By default, all non-deleted instances are counted.
    """

    def __init__(self, counter_name, foreign_field, is_in_counter=None):
        self.counter_name = counter_name
        self.foreign_field = foreign_field.field
        self.child_model = self.foreign_field.model
        self.parent_model = self.foreign_field.related_model

        if not is_in_counter:
            is_in_counter = lambda instance: True
        self.is_in_counter = is_in_counter

        self.connect()

    def validate(self):
        """
        Validate that this counter is indeed defined on the parent
        model.
        """
        counter_field, _, _, _ = self.parent_model._meta.get_field_by_name(
            self.counter_name
        )
        if not isinstance(counter_field, CounterCacheField):
            raise TypeError("%s should be a CounterCacheField on %s, but is %s" % (
                self.counter_name, self.parent_model, type(counter_field)))

    @property
    def was_in_counter_key(self):
        return f'{self.counter_name}_was_in_counter'

    def pre_save_receiver(self, instance, **kwargs):
        try:
            old_instance = instance.__class__.objects.get(pk=instance.pk)
            was_in_counter = self.is_in_counter(old_instance)
        except:
            was_in_counter = False
        setattr(instance, self.was_in_counter_key, was_in_counter)

    def post_save_receiver(self, instance, **kwargs):
        was_in_counter = getattr(instance, self.was_in_counter_key, False)
        try:
            delattr(instance, self.was_in_counter_key)
        except AttributeError:
            pass

        is_in_counter = self.is_in_counter(instance)
        if not was_in_counter and is_in_counter:
            self.increment(instance, 1)
        elif was_in_counter and not is_in_counter:
            self.increment(instance, -1)

    def post_delete_receiver(self, instance, **kwargs):
        if self.is_in_counter(instance):
            self.increment(instance, -1)

    def connect(self):
        """
        Register a counter between a child model and a parent.
        """
        name = "%s.%s.%s" % (
            self.parent_model._meta.model_name,
            self.child_model._meta.model_name,
            self.foreign_field.name
        )
        counted_name = "%s-%s" % (name, self.counter_name)

        def pre_save_receiver_counter(sender, instance, **kwargs):
            self.pre_save_receiver(instance)

        pre_save.connect(pre_save_receiver_counter, sender=self.child_model, weak=False,
                         dispatch_uid=f'{counted_name}_pre_save')

        def post_save_receiver_counter(sender, instance, **kwargs):
            self.post_save_receiver(instance)

        post_save.connect(post_save_receiver_counter, sender=self.child_model, weak=False,
                          dispatch_uid=f'{counted_name}_post_save')

        def post_delete_receiver_counter(sender, instance, **kwargs):
            self.post_delete_receiver(instance)

        post_delete.connect(post_delete_receiver_counter, sender=self.child_model, weak=False,
                            dispatch_uid=f'{counted_name}_post_delete')

        counters[counted_name] = self

    def parent_id(self, child):
        """
        Returns the id of the parent that includes the given *child*
        instance in its counter.
        """
        return getattr(child, self.foreign_field.attname)

    def set_counter_field(self, parent_id, value):
        """
        Set the value of a counter field on *parent_id* to *value*.
        """
        return self.parent_model.objects.filter(pk=parent_id).update(**{
            self.counter_name: value
        })

    def increment(self, child, amount):
        """
        Increment a counter using a *child* instance to find the the
        parent. Pass a negative amount to decrement.
        """
        parent_id = self.parent_id(child)
        return self.set_counter_field(parent_id, F(self.counter_name) + amount)


def connect_counter(counter_name, foreign_field, is_in_counter=None):
    """
    Register a counter between a child model and a parent. The parent
    must define a CounterCacheField field called *counter_name* and the child
    must reference its parent using a ForeignKey *foreign_field*. Supply
    an optional callback function *is_in_counter* for over which child
    instances to count.
    By default, all persisted (non-deleted) child instances are counted.

    Arguments:
    counter_name - The name of the counter. A CounterCacheField field with
    this name must be defined on the parent model.
    foreign_field - A ForeignKey field defined on the counted child
    model. The foreign key must reference the parent model.
    is_in_counter - The callback function is_in_counter will be given
    instances of the counted model. It must return True if the instance
    qualifies to be counted, and False otherwise. The callback should
    not concern itself with checking if the instance is deleted or not.
    """
    return Counter(counter_name, foreign_field, is_in_counter)
