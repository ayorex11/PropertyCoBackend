from rest_framework import serializers
from .models import Message, AdminMessage
from properties.serializers import PropSerializer


class MiniMessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()

	class Meta:
		model = Message
		fields = ['id','sender', 'subject', 'date_created', 'read']


class AdminMiniMessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()

	class Meta:
		model = AdminMessage
		fields = ['id','sender', 'subject', 'date_created', 'read']

class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()
	receiver = serializers.StringRelatedField()

	class Meta:
		model = Message
		fields = '__all__'
		read_only_fields = ['sender','receiver', 'date_created', 'read', 'prop']


class AdminMessageSerializer(serializers.ModelSerializer):

	class Meta:
		model = AdminMessage
		fields = '__all__'
		read_only_fields = ['sender','date_created', 'read']

class SentMessageSerializer(serializers.ModelSerializer):
	receiver = serializers.StringRelatedField()


	class Meta:
		model = Message
		fields = ['id','receiver', 'subject', 'date_created']


class AdminSentMessageSerializer(serializers.ModelSerializer):
	receiver = serializers.StringRelatedField()


	class Meta:
		model = AdminMessage
		fields = ['id','receiver', 'subject', 'date_created']


class MainMessageSerializer(serializers.ModelSerializer):
	prop = PropSerializer()
	sender = serializers.StringRelatedField()
	receiver = serializers.StringRelatedField()

	class Meta:
		model = Message
		fields = '__all__'
		read_only_fields = ['sender','receiver', 'date_created']



class AdminMainMessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()
	receiver = serializers.StringRelatedField()

	class Meta:
		model = AdminMessage
		fields = '__all__'
		read_only_fields = ['sender','receiver', 'date_created']