from rest_framework import serializers
from .models import Blog



class miniserializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        exclude = ['draft',]
        


class Blogserializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        exclude = ['draft',]
        read_only_fields = ['date_created',]
