from rest_framework import serializers
from .models import Inspection
from Favorites.serializers import StringFavoriteSerializer, InspectpropFavoriteSerializer


class CreateInspectionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Inspection
        fields = '__all__'
        read_only_fields = ['user', 'inspection_id', 'date_created', 'district']

    def validate(self, data):
        if 'prop_1' not in data:
            raise serializers.ValidationError("prop_1 is required")
        
        return data


class InspectionSerializer(serializers.ModelSerializer):
	prop_1 = StringFavoriteSerializer()
	prop_2 = StringFavoriteSerializer()
	prop_3 = StringFavoriteSerializer()
	user = serializers.StringRelatedField()

	class Meta:
		model = Inspection
		fields = '__all__'

class MiniInspectionSerializer(serializers.ModelSerializer):
	prop_1 = InspectpropFavoriteSerializer()
	prop_2 = InspectpropFavoriteSerializer()
	prop_3 = InspectpropFavoriteSerializer()

	class Meta:
		model = Inspection
		fields = ['id', 'inspection_id','prop_1', 'prop_2', 'prop_3', 'date_created', 'district', 'date', 'timeslot']
		
