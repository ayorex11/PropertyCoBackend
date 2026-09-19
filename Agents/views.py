from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, NProfileSerializer, UpdateRatingSerializer
from .models import Profile
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FormParser, MultiPartParser
from notifs.models import AgentNotification
from datetime import datetime
from rating_history.models import History


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_profile(request):
	user=request.user
	if user.account_type == 'User' :
		return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		profile = Profile.objects.get(user=user)
	except:
		profile = Profile.objects.create(user=user, contact_number=user.phone_number, first_name=user.first_name, last_name=user.last_name, email_address = user.email, member_id=user.member_id)
	serializer=ProfileSerializer(profile, many=False)
	data={'message':'success',
		'data':serializer.data}
	return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=["PATCH"], request_body=NProfileSerializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])

def update_profile(request):
	user = request.user
	if user.account_type == 'User':
		return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
	profile = get_object_or_404(Profile, user=user)
	serializer = NProfileSerializer(profile, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save(user=request.user)
	data = {'message': 'success',
			'data':serializer.data}
	return Response (data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_all_agents(request):
	user = request.user
	xyz = Profile.objects.all()
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

	serializer = ProfileSerializer(xyz, many=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agent_by_email(request, email):
	user = request.user
	try:
		xyz = Profile.objects.get(email_address=email)
	except Profile.DoesNotExist:
		raise Http404
	if user.is_admin == False:
		return Response({'message':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer = NProfileSerializer(xyz, many=False)
	data = {'message':'success',
			'data':serializer.data}
	return Response(data, status=status.HTTP_200_OK)



@swagger_auto_schema(methods=["PATCH"], request_body=UpdateRatingSerializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def update_agent_rating(request, member_id):
    user = request.user
    profile = get_object_or_404(Profile, member_id=member_id)

    # Check if the user is an admin
    if not user.is_admin:
        return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    prev_rating = profile.rating

    serializer = UpdateRatingSerializer(profile, data=request.data)
    serializer.is_valid(raise_exception=True)
    new_rating = serializer.validated_data.get('rating')

    rating_change = float(new_rating) - float(prev_rating)
    date = datetime.now()

    # Update the existing profile rating instead of creating a new one
    profile.rating = new_rating
    profile.save()

    # Determine rating change description
    if rating_change == 0:
        rating_str = 'No change made'
    elif rating_change < 0:
        rating_str = f"-{abs(rating_change)}"
    else:
        rating_str = f"+{rating_change}"

    reason = serializer.validated_data.get('reason')

    # Create history entry
    hist = History(user=profile.user, rating=rating_str, reason=reason, date=date)
    hist.save()

    # Create notification for the user
    title = 'Your Profile/User rating has been updated'
    body = 'Your Profile has been updated by the Admin, check your dashboard out'
    notif = AgentNotification(user=profile.user, title=title, body=body, date_created=date, read=False)
    notif.save()

    data = {
        'message': 'success',
        'data': serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def verify_user(request, member_id):
    user = request.user
    if not user.is_admin:
        return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    prof = get_object_or_404(Profile, member_id=member_id)
    prof.verified = True
    prof.save()

    date = datetime.now()
    title = 'Your Profile has been updated'
    body = 'Your Profile has been updated by the Admin, check your dashboard out'
    notif = AgentNotification(user=prof.user, title=title, body=body, date_created=date, read=False)
    notif.save()

    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def unverify_user(request, member_id):
    user = request.user
    if not user.is_admin:
        return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    prof = get_object_or_404(Profile, member_id=member_id)
    prof.verified = False
    prof.save()

    date = datetime.now()
    title = 'Your Profile has been updated'
    body = 'Your Profile has been updated by the Admin, check your dashboard out'
    notif = AgentNotification(user=prof.user, title=title, body=body, date_created=date, read=False)
    notif.save()

    return Response({'message': 'success'}, status=status.HTTP_200_OK)

