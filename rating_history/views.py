from django.shortcuts import render
from .models import  History
from .serializers import  HistorySerializer
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes, parser_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from Account.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_history(request):
	user = request.user 
	if user.is_admin == False:
		return Response({'message':'Unauthorized Reqquest'}, status=status.HTTP_401_UNAUTHORIZED)

	book = History.objects.all()
	serializer = HistorySerializer(book, many=True)

	data ={'message': 'success',
			'data': serializer.data}

	return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request, email):
	user = request.user 
	users = User.objects.get(email=email)
	if user.is_admin == False:
		return Response({'message':'Unauthorized Reqquest'}, status=status.HTTP_401_UNAUTHORIZED)

	book = History.objects.filter(user=users)
	serializer = HistorySerializer(book, many=True)

	data ={'message': 'success',
			'data': serializer.data}

	return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_history(request):
	user = request.user 

	book = History.objects.filter(user=user)
	serializer = HistorySerializer(book, many=True)

	data ={'message': 'success',
			'data': serializer.data}

	return Response(data=data, status=status.HTTP_200_OK)
