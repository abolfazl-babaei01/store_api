from django.db import models
from accounts.models import CustomUser


class Notification(models.Model):
    """
    Represents a notification sent to a specific user.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ({self.id})'

    def mark_as_read(self):
        """
        Marks the notification as read.
        """
        self.is_read = True
        self.save()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
