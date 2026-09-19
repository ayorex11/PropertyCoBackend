from rest_framework import permissions, status, generics
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite_property
from django.shortcuts import get_object_or_404
from django.http import Http404
from Agents.models import Profile
from rest_framework.generics import CreateAPIView
from properties.models import Property
from rest_framework.permissions import IsAuthenticated
from .serializers import FavoriteSerializer, StringFavoriteSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FavoritePropertyCreateView(CreateAPIView):
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        # Get the property id from the request data
        prop_id = request.data.get('prop', None)
        
        # Check if the property with the given id exists
        property_instance = get_object_or_404(Property, id=prop_id)

        # Check if the user has already favorited the property
        user = self.request.user
        existing_favorite = Favorite_property.objects.filter(user=user, prop=property_instance)

        if existing_favorite.exists():
            return Response({'detail': 'You have already favorited this property.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new favorite
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class get_favorites(APIView):
    permissions = (permissions.IsAuthenticated,)
    serializer_class = StringFavoriteSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        prop = Favorite_property.objects.filter(user=user)
        serializer = StringFavoriteSerializer(prop, many=True)

        return Response({'message':'success', 'data':serializer.data}, status=status.HTTP_200_OK )

class remove_favorite(APIView):
	permissions = (permissions.IsAuthenticated,)
	serializer_class = FavoriteSerializer


	def delete(self, request, pk,  *args, **kwargs):
		user = request.user
		prop = Favorite_property.objects.get(id=pk)
		if prop.user != user:
			return Response ({'message':'object cant be deleted'}, status=status.HTTP_400_BAD_REQUEST)
		prop.delete()
		return Response({'message': 'Favorite property deleted'}, status=status.HTTP_200_OK)
