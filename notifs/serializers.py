from rest_framework import serializers
from .models import Notification, AgentNotification

class NotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Notification
		fields = '__all__'


class AgentNotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = AgentNotification
		exclude = ['user', ]