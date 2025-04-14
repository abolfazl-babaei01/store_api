from datetime import timedelta
from django.utils import timezone

def auto_block_ticket(ticket):
    last_message = ticket.messages.order_by('-created_at').first()
    if last_message:
        if timezone.now() - last_message.created_at > timedelta(days=2):
            ticket.is_blocked = True
            ticket.save()
