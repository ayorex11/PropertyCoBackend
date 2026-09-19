from rest_framework import serializers
from .models import Property

class MiniPropSerializer(serializers.ModelSerializer):
	agent = serializers.StringRelatedField()
	class Meta:
		model = Property
		fields = ['id','agent','picture1','featured', 'property_id', 'price', 'price_options', 'name', 'description','payment_options', 'initial_deposit', 'beds', 'bathrooms', 'toilets', 'created_at']

class PropertySerializer(serializers.ModelSerializer):
	agent = serializers.StringRelatedField()
	class Meta:
		model = Property
		exclude= ['featured',]
		read_only_fields = ['agent', 'created_at',]

class PropSerializer(serializers.ModelSerializer):
	agent = serializers.StringRelatedField()
	class Meta:
		model = Property
		fields = ['id','agent','name', 'category', 'prop_type', 'address', 'picture1', 'district', 'sub_location', 'price', 'serviced', 'inside_an_estate', 'swimming_pool', 'gym', 'electricity', 'price_options', 'created_at', 'description', 'payment_options', 'initial_deposit', 'property_id', 'furnished', 'newly_built', 'shared', 'beds', 'bathrooms', 'toilets', 'featured']

class CreatePropSerializer(serializers.ModelSerializer):

	class Meta:
		model = Property
		exclude = ['featured',]
		read_only_fields = ['agent', 'created_at', 'updated_at','property_id', 'approved', 'disapproved']
		


class InspectpropSerializer(serializers.ModelSerializer):

	class Meta:
		model = Property
		fields = [ 'property_id',]

