from django.db.models import ForeignObject, ManyToManyField
from rest_framework import viewsets

from django_audit_events.filters import AuditEventFilterSet
from django_audit_events.models import get_audit_event_model
from django_audit_events.serializers import EventSerializer


class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_audit_event_model().objects.all()
    filter_class = AuditEventFilterSet
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super(AuditEventViewSet, self).get_queryset()
        # noinspection PyProtectedMember
        fields = queryset.model._meta.local_fields
        select_related = []
        prefetch_related = []

        for field in fields:
            if isinstance(field, ForeignObject):
                select_related.append(field.name)
            elif isinstance(field, ManyToManyField):
                prefetch_related.append(field.name)

        return queryset.select_related(*select_related).prefetch_related(
            *prefetch_related
        )
