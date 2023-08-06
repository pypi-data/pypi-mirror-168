Advanced Usage
==============

Django Audit Events app is highly extensible.

Common content for multiple events
----------------------------------

The audit context can store extra data to be present in every event it creates.

.. code-block:: python

    audit_context = AuditContext()
    audit_context.extra_data["foo"] = "bar"
    event = audit_context.new_event()
    assert event.content["foo"] == "bar"

You can even override this data for a single event if you need.

.. code-block:: python

    audit_context = AuditContext()
    audit_context.extra_data["foo"] = "bar"
    event = audit_context.create_event(content_object, foo="baz")
    assert event.content["foo"] == "baz"

Swapping event model
--------------------

You can create your own audit event models by extending ``django_audit_events.models.AbstractAuditEvent``.

.. code-block:: python

    class MyEvent(AbstractAuditEvent):
        ...

        class Meta(AbstractAuditEvent.Meta):
            swappable = "AUDIT_EVENT_MODEL"

Archiving aged audit events
---------------------------

Old audit events may be archived in order to prevent database from being overloaded.

.. code-block:: python

    from celery.schedules import crontab

    CELERYBEAT_SCHEDULE = {
        "archive-old-audit-events": {
            "task": "django_audit_events.tasks.archive_old_audit_events",
            "schedule": crontab(hour=0, minute=0),
            "args": (),
            "kwargs": {"older_than": 90}
        },
    }

Using ``CELERYBEAT_SCHEDULE`` configuration like one above, audit events older than
90 days will be archived every day.
