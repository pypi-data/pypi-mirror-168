Introduction
============

Installation
------------

You can install this package from `PyPI <https://pypi.org/>`_::

    pip install django-audit-events

You need to append it to the ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_audit_events',
    ]

And the ``MIDDLEWARE``:

.. code-block:: python

    MIDDLEWARE = [
        ...
        'django_audit_events.middleware.AuditEventsMiddleware',
    ]

Then migrate your project::

    python manage.py migrate

Now you are ready to create your events, take a look at :doc:`quickstart`.

Philosophy
----------

django-audit-events is the product of the following technical decisions.

* All events must be associated with one content object. Everything else is optional.
* Events should not be created automatically (or magically), because "Explicit is better than implicit".
* Multiple events can be created when processing a single request.
* Events may be created without an HTTP request, such as a `Celery <http://www.celeryproject.org/>`_ task or a management command.
* Developers should not need to check if an audit context exists or not when creating events. That is the reason why ``AuditContextMixin`` always creates a blank audit context.
