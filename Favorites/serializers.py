from rest_framework import serializers
from .models import Favorite_property
from properties.serializers import PropSerializer, InspectpropSerializer

class FavoriteSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()

	class Meta:
		model = Favorite_property
		fields =  ['id','prop','user']
		read_only_fields = ['user',]


class StringFavoriteSerializer(serializers.ModelSerializer):

	prop = PropSerializer()

	class Meta:
		model = Favorite_property
		fields =  ['id','prop']


class InspectpropFavoriteSerializer(serializers.ModelSerializer):

	prop = InspectpropSerializer()

	class Meta:
		model = Favorite_property
		fields =  ['prop',]
