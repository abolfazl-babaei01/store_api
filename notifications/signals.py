from django.db.models.signals import post_save
from django.dispatch import receiver
from ticket.models import TicketMessage
from .models import Notification

@receiver(post_save, sender=TicketMessage)
def create_notification_for_admin_reply(sender, instance, created, **kwargs):
    """
    Creates a notification for the user when an admin replies to their ticket.
    """
    if created and instance.is_admin_reply:
        Notification.objects.create(
            user=instance.ticket.user,
            message=f"Admin replied to your ticket: {instance.ticket.subject}",
        )
