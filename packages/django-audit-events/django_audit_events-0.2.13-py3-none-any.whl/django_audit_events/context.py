from copy import deepcopy

from django.apps import apps
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string

from django_audit_events.conf import settings

MASK_VALUE = "*" * 16


class AuditContext(object):
    extra_data = {}
    __slots__ = ["url", "remote_addr", "user", "query_params", "post_data", "headers"]

    def __init__(
        self,
        url=None,
        remote_addr=None,
        user=None,
        query_params=None,
        post_data=None,
        headers=None,
    ):
        super(AuditContext, self).__setattr__("url", url)
        super(AuditContext, self).__setattr__("remote_addr", remote_addr)
        super(AuditContext, self).__setattr__("user", user)
        super(AuditContext, self).__setattr__("query_params", query_params or {})
        super(AuditContext, self).__setattr__("post_data", post_data or {})
        super(AuditContext, self).__setattr__("headers", headers or {})

    def __setattr__(self, key, value):
        raise NotImplementedError

    def __delattr__(self, item):
        raise NotImplementedError

    @classmethod
    def from_request(cls, request):
        """
        Create a context from HTTP request

        :type request: django.http.HttpRequest
        :return: An audit context
        :rtype: AuditContext
        """
        # noinspection PyUnresolvedReferences
        client_ip_function = cls.get_client_ip_function()
        context = {
            "url": request.build_absolute_uri(),
            "remote_addr": client_ip_function(request),
            "user": request.user,
        }

        if isinstance(context["user"], AnonymousUser):
            context["user"] = None

        if settings.AUDIT_INCLUDE_QUERY_PARAMS:
            context["query_params"] = request.GET

        if settings.AUDIT_INCLUDE_POST_DATA:
            # Copy POST data before masking sensitive fields
            # noinspection PyArgumentList
            context["post_data"] = cls.mask_fields(
                request.POST.copy(),
                settings.AUDIT_MASK_POST_FIELDS,
            )

        if settings.AUDIT_INCLUDE_HEADERS and isinstance(
            settings.AUDIT_INCLUDE_HEADERS, list
        ):
            context["headers"] = {
                header.replace("HTTP_", "", 1)
                .replace("_", "-")
                .title(): request.META.get(header)
                for header in settings.AUDIT_INCLUDE_HEADERS
                if request.META.get(header)
            }

        return cls(**context)

    @staticmethod
    def mask_fields(data, fields_to_mask):
        """
        Replace sensitive information in POST data
        :param data: POST data
        :type data: dict|django.http.request.QueryDict
        :param fields_to_mask: Names of fields to mask
        :type fields_to_mask: tuple|list
        :return: Data with masked sensitive information
        :rtype: dict
        """
        for field in filter(lambda x: x in data, fields_to_mask):
            data[field] = MASK_VALUE
        return data

    def new_event(self):
        """
        :return: Unsaved audit event
        :rtype: django_audit_events.models.AbstractAuditEvent
        """
        model = apps.get_model(settings.AUDIT_EVENT_MODEL)
        event = model.from_context(self)
        event.content = deepcopy(self.extra_data)
        return event

    def create_event(self, content_object, **content):
        """
        :param content_object: Object for the audit event
        :param content: Event content
        :return: Saved audit event
        :rtype: django_audit_events.models.AbstractAuditEvent
        """
        event = self.new_event()
        event.content_object = content_object
        event.content.update(content)
        event.save()
        return event

    def create_fields_event(self, content_object, *fields, **content):
        """
        :param content_object: Object for the audit event
        :param fields: Fields to store in the event
        :param content: Event content
        :return: Saved audit event
        :rtype: django_audit_events.models.AbstractAuditEvent
        """
        for field in fields:
            content[field] = getattr(content_object, field)
        return self.create_event(content_object, **content)

    @classmethod
    def get_client_ip_function(cls):
        _function = settings.AUDIT_CLIENT_IP_RESOLVER_FUNCTION
        if callable(_function):
            return _function
        return import_string(_function)
