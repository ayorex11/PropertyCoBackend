from rest_framework import serializers
from .models import Request

class RequestPropertySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ['user',]
