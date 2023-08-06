from django.contrib import admin

from django_audit_events.models import ArchivedAuditEvent, AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "content_object", "timestamp")


@admin.register(ArchivedAuditEvent)
class ArchivedAuditEventAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "content_object", "timestamp")
