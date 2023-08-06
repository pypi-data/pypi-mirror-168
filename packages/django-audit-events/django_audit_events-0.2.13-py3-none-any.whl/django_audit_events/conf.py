from django.conf import settings as django_settings

DEFAULT_SETTINGS = {
    "AUDIT_EVENT_MODEL": "django_audit_events.AuditEvent",
    "AUDIT_EVENT_ARCHIVE_MODEL": "django_audit_events.ArchivedAuditEvent",
    "AUDIT_INCLUDE_QUERY_PARAMS": False,
    "AUDIT_INCLUDE_POST_DATA": False,
    "AUDIT_INCLUDE_HEADERS": False,
    "AUDIT_MASK_POST_FIELDS": ("password",),
    "AUDIT_CLIENT_IP_RESOLVER_FUNCTION": "django_audit_events.utils.get_client_ip",
}


class Settings(object):
    def __getattr__(self, item):
        if item in DEFAULT_SETTINGS:
            return getattr(django_settings, item, DEFAULT_SETTINGS[item])
        raise AttributeError


settings = Settings()
