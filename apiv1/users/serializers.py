from rest_framework.serializers import ModelSerializer

from users.models import Notification

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'