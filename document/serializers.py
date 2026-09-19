from rest_framework import serializers
from .models import Docunment

class DocunmentSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	class Meta:
		model = Docunment
		fields = '__all__'
		read_only_fields = ['user',]