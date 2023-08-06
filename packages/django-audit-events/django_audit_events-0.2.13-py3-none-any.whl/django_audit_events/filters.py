from rest_framework_filters import FilterSet, filters

from django_audit_events.models import get_audit_event_model


class AuditEventFilterSet(FilterSet):
    user = filters.NumberFilter(name="user")
    content_type = filters.NumberFilter(name="content_type")
    object_id = filters.NumberFilter(name="object_id")
    timestamp = filters.AllLookupsFilter(
        name="timestamp",
        lookups=["lt", "gt", "lte", "gte"],
        lookup_expr=["lt", "gt", "lte", "gte"],
    )

    class Meta:
        model = get_audit_event_model()
        fields = ("user", "content_type", "object_id", "timestamp")
