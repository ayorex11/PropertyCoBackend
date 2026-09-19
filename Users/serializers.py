from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	class Meta:
		model = UserProfile
		fields = '__all__'
		read_only_fields = ['user', 'email_address', 'verified', 'member_id', 'created_at']


class UserNProfileSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	class Meta:
		model = UserProfile
		fields = '__all__'
		read_only_fields = ['user', 'email_address', 'verified', 'member_id', 'created_at']