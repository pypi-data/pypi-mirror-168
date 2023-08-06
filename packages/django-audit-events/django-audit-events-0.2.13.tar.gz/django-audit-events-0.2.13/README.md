# Django Audit Events

[![Build status](https://img.shields.io/bitbucket/pipelines/akinonteam/django-audit-events)](https://bitbucket.org/akinonteam/django-audit-events/addon/pipelines/home)
[![Documentation status](https://readthedocs.org/projects/django-audit-events/badge/?version=latest)](https://django-audit-events.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/django-audit-events)
![PyPI - Django version](https://img.shields.io/pypi/djversions/django-audit-events)
![PyPI - Python version](https://img.shields.io/pypi/pyversions/django-audit-events)
![PyPI - License](https://img.shields.io/pypi/l/django-audit-events)
[![Total alerts](https://img.shields.io/lgtm/alerts/bitbucket/akinonteam/django-audit-events)](https://lgtm.com/projects/b/akinonteam/django-audit-events/alerts/)
[![Code quality](https://img.shields.io/lgtm/grade/python/bitbucket/akinonteam/django-audit-events)](https://lgtm.com/projects/b/akinonteam/django-audit-events/context:python)

Extensible custom audit events for humans! This Django app allows you to easily create your own events in your project. Currently only works on PostgreSQL.

Let's have a look:

```python
def awesome_view(request):
    foo_obj = Foo.objects.get(pk=1)
    # Do something with foo_obj...
    request.audit_context.create_event(
        foo_obj,
        something="done",
        bar="baz"
    )
```

This will create an audit event, including the request URL, logged-in user, remote IP address, and the following event content:

```
>>> event.content
{"something": "done", "bar: "baz"}
```

For more information about installation and usage, check out the [documentation](https://django-audit-events.readthedocs.io/)!
