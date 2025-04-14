from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Ticket(models.Model):
    """
    Model representing a support ticket created by a user.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tickets'  # Reverse relation: user.tickets.all()
    )
    subject = models.CharField(max_length=100)  # Subject/title of the ticket
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.subject} by {self.user}'


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class TicketMessage(models.Model):
    """
    Model representing a message within a support ticket thread.
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages'  # Reverse relation: ticket.messages.all()
    )
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ticket_messages'  # Reverse relation: user.ticket_messages.all()
    )
    is_admin_reply = models.BooleanField(default=False)  # Indicates if the message is sent by an admin
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket.subject

    class Meta:
        ordering = ['created_at']  # Messages ordered from oldest to newest
