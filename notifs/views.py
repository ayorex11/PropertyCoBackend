from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer, AgentNotificationSerializer
from .models import Notification, AgentNotification
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
	user = request.user
	xyz = Notification.objects.all()
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = NotificationSerializer(xyz, many=True)
	data = {'message':'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, pk):
	user = request.user
	xyz = Notification.objects.get(id=pk)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	xyz.read = True
	xyz.save()
	serializer = NotificationSerializer(xyz, many=False)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_notifications(request):
	user = request.user
	xyz = AgentNotification.objects.filter(user=user)

	serializer = AgentNotificationSerializer(xyz, many=True)
	data = {'message':'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_read(request, pk):
	user = request.user
	xyz = AgentNotification.objects.get(id=pk)
	if xyz.user != user:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	xyz.read = True
	xyz.save()
	serializer = AgentNotificationSerializer(xyz, many=False)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


