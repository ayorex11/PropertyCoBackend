from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User 
from django.http import Http404
from Agents.models import Profile

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_all_users(request):
	user = request.user
	xyz = User.objects.all()
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = UserSerializer(xyz, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_all_agents(request):
	user = request.user
	xyz = User.objects.filter(account_type='Agent')
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = UserSerializer(xyz, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_all_nonagents(request):
	user = request.user
	xyz = User.objects.filter(account_type='User')
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = UserSerializer(xyz, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_email(request, email):
	user = request.user
	try:
		xyz = User.objects.get(email=email)
	except User.DoesNotExist:
		raise Http404
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer = UserSerializer(xyz, many=False)
	prof = Profile.objects.get(user=xyz)
	data = {}
	data['message'] = 'success'
	data['data'] = serializer.data
	data['address'] = prof.address
	data['rating']= prof.rating
	return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_member_id(request, member_id):
	user = request.user
	try:
		xyz = User.objects.get(member_id=member_id)
	except User.DoesNotExist:
		raise Http404
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer = UserSerializer(xyz, many=False)
	data = {'message':'success',
			'data':serializer.data}
	return Response(data, status=status.HTTP_200_OK)
