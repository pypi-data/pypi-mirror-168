import logging
from datetime import timedelta

from celery import current_app as app
from django.db import transaction
from django.utils import timezone

from django_audit_events.models import (
    get_audit_event_archive_model,
    get_audit_event_model,
)

logger = logging.getLogger(__name__)


def _chunks(items, chunks_size=200):
    index, _items = 0, items
    while _items:
        _items = items[index * chunks_size : (index + 1) * chunks_size]
        if _items:
            yield _items
        index += 1


@app.task
def archive_old_audit_events(older_than=90):
    audit_event_model = get_audit_event_model()
    archived_audit_event_model = get_audit_event_archive_model()

    reference_date = timezone.now() - timedelta(days=older_than)
    events_to_delete = set()

    for event in audit_event_model.objects.iterator():
        if event.content_object is None:
            events_to_delete.add(event.uuid)

    events_to_delete = list(events_to_delete)

    for chunk in _chunks(events_to_delete):
        with transaction.atomic():
            audit_event_model.objects.filter(uuid__in=[e for e in chunk]).delete()

    events_to_archive = audit_event_model.objects.filter(timestamp__lte=reference_date)
    archive_items = [event.as_archive_event() for event in events_to_archive]

    for chunk in _chunks(archive_items):
        with transaction.atomic():
            archived_audit_event_model.objects.bulk_create(chunk)
            audit_event_model.objects.filter(uuid__in=[e.uuid for e in chunk]).delete()

    logger.info("Archived %d audit events." % events_to_archive.count())
    logger.info("Deleted %d audit events." % len(events_to_delete))
