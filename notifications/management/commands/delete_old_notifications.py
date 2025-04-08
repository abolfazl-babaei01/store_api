from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Delete read notifications older than 1 day'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=1)
        deleted, _ = Notification.objects.filter(is_read=True, created_at__lt=cutoff).delete()
        self.stdout.write(f"{deleted} notifications deleted.")