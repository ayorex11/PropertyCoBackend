from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes, parser_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import DocunmentSerializer
from .models import Docunment
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FormParser, MultiPartParser
from notifs.models import Notification
from datetime import datetime
from Agents.models import Profile
from Account.models import User


@swagger_auto_schema(methods=["POST"], request_body=DocunmentSerializer())
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])

def upload(request):
	user = request.user
	if Docunment.objects.filter(user=user).exists():
		return Response({"message": "Docunments exist already"}, status=status.HTTP_400_BAD_REQUEST)
	serializer = DocunmentSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save(user = user)
	title = 'New Docunment uploaded'
	body = f'User {user} has uploaded their Docunments.'
	date_created = datetime.now()
	read = False
	notif = Notification(title=title, body=body, date_created=date_created, read=read)
	notif.save()

	return Response({"message": "success"}, status=status.HTTP_201_CREATED)



@swagger_auto_schema(methods=["PATCH"], request_body=DocunmentSerializer())
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes({FormParser, MultiPartParser})

def update_docunments(request):
	user = request.user 
	agent = Profile.objects.get(user=user)
	doc = get_object_or_404(Docunment, user=user)
	serializer = DocunmentSerializer(doc, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save(user=user)
	title = 'Docunments updated'
	body = f'User {user} has updated their Docunments.'
	date_created = datetime.now()
	read = False
	agent.verified = False
	agent.save()
	notif = Notification(title=title, body=body, date_created=date_created, read=read)
	notif.save()
	return Response({"message": "success"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_all_docunments(request):
	user = request.user 
	docs = Docunment.objects.all()
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = DocunmentSerializer(docs, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)
	


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_my_docunment(request):
	user = request.user 
	docs = get_object_or_404(Docunment, user=user)

	serializer = DocunmentSerializer(docs)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_user_docunment(request, email_address):
	user = request.user
	if not user.is_admin:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
	Prof = get_object_or_404(User, email=email_address)
	docunment = get_object_or_404(Docunment, user=Prof)
	serializer = DocunmentSerializer(docunment, many=False)
	data = {
		'message':'success',
		'data': serializer.data
	}
	return Response(data=data, status=status.HTTP_200_OK)