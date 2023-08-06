from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_audit_events.models import get_audit_event_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "email", "first_name", "last_name")


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = "__all__"
        model = get_audit_event_model()
