=========================
django_counter_cache_fuxy
=========================
.. image:: https://travis-ci.org/enjoy2000/django-counter-cache-field.svg?branch=master
    :target: https://travis-ci.org/enjoy2000/django-counter-cache-field


.. image:: https://coveralls.io/repos/github/enjoy2000/django-counter-cache-field/badge.svg
    :target: https://coveralls.io/github/enjoy2000/django-counter-cache-field


It is sometimes useful to cache the total number of objects associated with another object through a ForeignKey
relation. For example the total number of comments associated with an article.

django_counter_cache_fuxy makes it easy to denormalize and keep such counters up to date.

Quick start
-----------

1. Install django_counter_cache_fuxy::

    pip install django_counter_cache_fuxy

2. Add "django_counter_cache_fuxy" to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
        ...
        'django_counter_cache_fuxy',
    )

3. Add a CounterCacheField to your model::

    from django_counter_cache_fuxy import CounterCacheField


    class Article(models.Model):
        comment_count = CounterCacheField()

4. Connect the related foreign key field with the counter field in your signals::

    connect_counter('comment_count', Comment.article)

Whenever a comment is created the comment_count on the associated Article will be incremented. If the comment is
deleted, the comment_count will be automatically decremented.


Overview
--------

Creating a new counter requires three simple steps:

1. Add a `CounterCacheField` field to the parent model.
2. Add the `CounterMixin` mixin to the child model.
3. Use `connect_counter` to connect the child model with the new counter.

Most counters are simple in the sense that you want to count all child objects. Sometimes, however, objects should be
counted based on one or several conditions. For example you may not wish to count *all* comments on an article but
only comments that have been approved. You can create conditional counters by providing a third `is_in_counter_func`
argument to `connect_counter`:

    connect_counter('comment_count', Comment.article, lambda comment: comment.is_approved)

The `is_in_counter_func` function will be called with `Comment` objects and must return `True` if the given comment
should be counted. It must not concern itself with checking if the comment is deleted or not, django_counter_cache_fuxy
does that by default.

Backfilling
-----------

Often you will add a `CounterCacheField` to a model that already has a large number of associated objects. When a counter
is created, it's value is initialized to zero. This value is likely incorrect. django_counter_cache_fuxy provides a couple
of management commands that allow you to rebuild the value of a counter:

1. List all available counters:

    $ python manage.py list_counters

2. Rebuild a counter using one of the counter names given by `list_counters`:

    $ python manage.py rebuild_counter <counter_name>

Note: The `rebuild_counter` management command will only update counters on objects that have at least one child
object. For example articles with at least one comment. Articles with no comments  will not be updated. This
is a conscious limitation; the use cases for such a feature seem very limited, if existent at all.


Documentation
-------------

    $ pip install Sphinx
    $ cd docs
    $ make html
    Open build/html/index.html
