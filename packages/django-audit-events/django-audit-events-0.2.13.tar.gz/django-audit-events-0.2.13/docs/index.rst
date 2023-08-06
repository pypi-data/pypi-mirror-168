Django Audit Events
===================

Extensible custom audit events for humans! This Django app allows you to easily create your own events in your project. Currently only works on PostgreSQL.

Let's have a look:

.. code-block:: python

    def awesome_view(request):
        foo_obj = Foo.objects.get(pk=1)
        # Do something with foo_obj...
        request.audit_context.create_event(
            foo_obj,
            something="done",
            bar="baz"
        )

This will create an audit event, including the request URL, logged-in user, remote IP address, and the following event content:

.. code-block:: python

    >>> event.content
    {"something": "done", "bar: "baz"}

The content may contain anything that is passed to ``create_event`` method as keyword arguments, as long as they are JSON serializable.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   quickstart
   configuration
   advanced
