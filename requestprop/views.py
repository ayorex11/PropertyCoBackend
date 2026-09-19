from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Request
from .serializers import RequestPropertySerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

class RequestProperty(CreateAPIView):
    serializer_class = RequestPropertySerializer
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        self.send_notification_email(serializer.data)
        return Response({'message': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def send_notification_email(self, data):
        user_email = data.get('user')
        template = render_to_string('main/request.html', data)
        email = EmailMessage(
            'New Property Request',
            template,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )
        email.send()
