from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, AdminMessage
from .serializers import (
    MiniMessageSerializer,
    MessageSerializer,
    AdminMessageSerializer,
    SentMessageSerializer,
    MainMessageSerializer,
    AdminMiniMessageSerializer,
    AdminSentMessageSerializer,
    AdminMainMessageSerializer,
)
from django.shortcuts import get_object_or_404
from django.http import Http404
from Agents.models import Profile
from Users.models import UserProfile
from rest_framework.generics import CreateAPIView
from properties.models import Property
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.exceptions import ParseError

User = get_user_model()


class UserMessageCreateView(CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        propertyid = request.data.get('property_id')
        prop = None

        if propertyid:
            try:
                prop = Property.objects.get(property_id=propertyid)
            except Property.DoesNotExist:
                return Response({'message': 'property not found'}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        
        receiver = get_object_or_404(User, is_admin=True)

        subject = request.data.get('subject')
        body = request.data.get('body')
        date_created = datetime.now()
        read = False

        message = Message(
            sender=sender,
            receiver=receiver,
            property_id=propertyid,
            prop=prop,
            subject=subject,
            body=body,
            date_created=date_created,
            read=read,
        )
        message.save()

        serializer = MessageSerializer(message)

        template = render_to_string('main/message.html', {'name': request.user.email})
        email = EmailMessage(
            'New Message',
            template,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )
        email.fail_silently = False
        email.send()


        data = {'message': 'successfully sent', 'data': serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)


class AdminMessageCreateView(CreateAPIView):
    serializer_class = AdminMessageSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        if not sender.is_admin:
            return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = request.data.get('receiver')
            receiver = User.objects.get(member_id=user_id)
        except (User.DoesNotExist, ParseError) as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

        subject = request.data.get('subject')
        body = request.data.get('body')
        date_created = datetime.now()
        read = False

        message = AdminMessage(
            sender=sender,
            receiver=receiver,
            subject=subject,
            body=body,
            date_created=date_created,
            read=read,
        )
        message.save()
        serializer = AdminMessageSerializer(message)

        template = render_to_string('main/message.html', {'name': request.user.email})
        email = EmailMessage(
            'New Message',
            template,
            settings.DEFAULT_FROM_EMAIL,
            [receiver.email],
        )
        email.fail_silently = False
        email.send()

        data = {'message': 'successfully sent', 'data': serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)


class GetMessages(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        mess = Message.objects.filter(receiver=user)
        serializer = MiniMessageSerializer(mess, many=True)
        data = {'message': 'success', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class UsersGetMessages(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        mess = AdminMessage.objects.filter(receiver=user)
        serializer = AdminMiniMessageSerializer(mess, many=True)
        data = {'message': 'success', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class GetSentMessages(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        mess = Message.objects.filter(sender=user)
        serializer = SentMessageSerializer(mess, many=True)
        data = {'message': 'success', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class AdminGetSentMessages(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        mess = AdminMessage.objects.filter(sender=user)
        serializer = AdminSentMessageSerializer(mess, many=True)
        data = {'message': 'success', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class GetMessageFully(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            mess = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        if mess.receiver != user:
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MainMessageSerializer(mess, many=False)
        data = {'message': 'success', 'sender_id': mess.sender.member_id, 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class UserGetMessageFully(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            mess = AdminMessage.objects.get(id=pk)
        except AdminMessage.DoesNotExist:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        if mess.receiver != user:
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminMainMessageSerializer(mess, many=False)
        data = {'message': 'success', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class ReadMessage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            mess = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        if mess.receiver != user:
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_400_BAD_REQUEST)

        mess.read = True
        mess.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class UserReadMessage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            mess = AdminMessage.objects.get(id=pk)
        except AdminMessage.DoesNotExist:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        if mess.receiver != user:
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_400_BAD_REQUEST)

        mess.read = True
        mess.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)
