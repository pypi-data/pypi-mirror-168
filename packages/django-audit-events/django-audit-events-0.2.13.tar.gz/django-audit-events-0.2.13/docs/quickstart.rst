Quick Start
===========

This page shows some examples of the basic usage. Audit events are created by the audit context. There are three methods for creating events:

.. glossary::
    ``new_event()``
        It only creates an event instance. All fields, including the ``content_object``, must be set by the developer. Also, after setting fields in the event, it must be saved.

    ``create_event(content_object, **content)``
        It creates an event instance and sets the ``content_object``. All other keyword arguments are stored in the ``content`` field of the event. Then the model is saved.

    ``create_fields_event(content_object, *fields, **content)``
        It behaves like ``create_event`` but additionally appends current field values to event content.

Creating events in views
------------------------

Since the audit context is available in the request object, events can easily be generated in views::

    def awesome_view(request, *args, **kwargs):
        foo_obj = Foo.objects.get(pk=1)
        # Do something with foo_obj...
        request.audit_context.create_event(
            foo_obj,
            something="done",
            bar="baz"
        )

You can still access the audit context from the request object, even if you have class-based views.

Creating events outside of the view scope
-----------------------------------------

If you want to create your audit events in your models or other classes, you can either pass audit_context as an argument or use ``AuditContextMixin``

Example using argument:

.. code-block:: python

    def my_function(arg1, arg2, audit_context=AuditContext(), *args, **kwargs):
        foo_obj = Foo.objects.get(pk=1)
        # Do something with foo_obj...
        audit_context.create_event(
            foo_obj,
            something="done",
            bar="baz"
        )

Example using mixin:

.. code-block:: python

    class Foo(models.Model, AuditContextMixin):
        ...

        def my_method(self):
            self.audit_context.create_event(self, ...)

You need to provide the audit context from view before running your method in the model:


.. code-block:: python

    foo_obj = Foo.objects.get(pk=1)
    foo_obj.audit_context = request.audit_context
    foo_obj.my_method()
