from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Partner
from .serializers import PartnerSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

class PartnerWithUs(CreateAPIView):
    serializer_class = PartnerSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.send_notification_email(serializer.data)
        return Response({'message': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def send_notification_email(self, data):
        template = render_to_string('main/partner.html', data)
        email = EmailMessage(
            'New Partner',
            template,
            settings.DEFAULT_FROM_EMAIL,
            [settings.SALES_NOTIFICATION_EMAIL],
        )
        email.send()