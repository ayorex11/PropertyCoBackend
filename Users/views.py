from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes, parser_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserProfileSerializer, UserNProfileSerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FormParser, MultiPartParser

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_profile(request):
	user=request.user
	if user.account_type != 'User':
		return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		profile = UserProfile.objects.get(user=user)
	except:
		profile = UserProfile.objects.create(user=user, contact_number=user.phone_number, first_name=user.first_name, last_name=user.last_name, email_address = user.email, member_id=user.member_id)
		
	serializer=UserProfileSerializer(profile, many=False)
	data={'message':'success',
		'data':serializer.data}
	return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=["PATCH"], request_body=UserNProfileSerializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def update_profile(request):
	user = request.user
	if user.account_type != 'User':
		return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
	profile = get_object_or_404(UserProfile, user=user)
	serializer = UserNProfileSerializer(profile, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save(user=request.user)
	data = {'message': 'success',
			'data':serializer.data}
	return Response (data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_non_agents(request):
	user = request.user
	xyz = UserProfile.objects.all()
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = UserProfileSerializer(xyz, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_non_agents_email(request, email):
	user = request.user
	try:
		xyz = UserProfile.objects.get(email_address=email)
	except UserProfile.DoesNotExist:
		raise Http404
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = UserProfileSerializer(xyz, many=False)
	data = {'message':'success',
			'data':serializer.data}
	return Response(data, status=status.HTTP_200_OK)

