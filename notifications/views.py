from rest_framework.response import Response
from rest_framework import generics, permissions, views
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    Returns a list of notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkAllNotificationsReadView(views.APIView):
    """
    Marks all unread notifications as read for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'detail': f'{count} notifications marked as read.'})
