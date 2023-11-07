from rest_framework import viewsets
from users.models import Notification
from .serializers import NotificationSerializer
from .paginations import NotificationPagination

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    pagination_class = NotificationPagination