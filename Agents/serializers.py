from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Profile        

class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()

	class Meta:
		model = Profile
		fields = '__all__'
		read_only_fields = ['user', 'rating', 'email_address', 'verified', 'member_id', 'created_at']


class NProfileSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()

	class Meta:
		model = Profile
		fields = '__all__'
		read_only_fields = ['user', 'rating', 'email_address', 'verified', 'member_id', 'created_at']


class UpdateRatingSerializer(serializers.Serializer):
	rating = serializers.DecimalField(max_digits=3, decimal_places=2, default=2.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
	reason = serializers.CharField(max_length=250, required=True, write_only =True)


		