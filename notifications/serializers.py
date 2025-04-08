from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for representing Notification instances.
    """
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
