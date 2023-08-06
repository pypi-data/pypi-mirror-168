import random
from datetime import timedelta

from django.db.models import Q
from django.test import TestCase, override_settings
from django.utils import timezone
from model_bakery import baker

from django_audit_events.models import ArchivedAuditEvent, AuditEvent
from django_audit_events.tasks import archive_old_audit_events
from django_audit_events.tests.utils.models import Poll


class ArchiveAuditEventTaskTestCase(TestCase):
    def setUp(self):
        events = [
            baker.prepare(AuditEvent, content_object=baker.make(Poll))
            for _ in range(100)
        ]
        AuditEvent.objects.bulk_create(events)
        for event in events:
            event.timestamp = self.get_random_past_date()
            event.save()

        for _ in range(25):
            random_event = random.choice(events)

            if random_event.content_object:
                random_event.content_object.delete()

            random_event.save()

    def tearDown(self):
        AuditEvent.objects.all().delete()
        ArchivedAuditEvent.objects.all().delete()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_archiver_task(self):
        older_than = 90
        query = Q(timestamp__lte=timezone.now() - timedelta(days=older_than))
        events_to_delete = set()

        for event in AuditEvent.objects.iterator():
            if event.content_object is None:
                events_to_delete.add(event.uuid)

        events_to_archive = AuditEvent.objects.filter(query).exclude(
            uuid__in=events_to_delete
        )
        uuids = set([e.uuid for e in events_to_archive])

        archive_old_audit_events(older_than=older_than)

        archived_events = ArchivedAuditEvent.objects.all()
        archived_uuids = set([e.uuid for e in archived_events])
        self.assertEqual(len(events_to_archive), len(archived_events))
        self.assertSetEqual(uuids, archived_uuids)
        self.assertFalse(AuditEvent.objects.filter(uuid__in=archived_uuids).exists())
        self.assertFalse(
            ArchivedAuditEvent.objects.filter(uuid__in=events_to_delete).exists()
        )
        self.assertFalse(AuditEvent.objects.filter(uuid__in=events_to_delete).exists())

    def get_random_past_date(self, base=timezone.now, date_range=timedelta(days=365)):
        if callable(base):
            base = base()
        seconds = date_range.total_seconds()
        minus_seconds = random.randint(0, seconds)
        return base - timedelta(seconds=minus_seconds)
