from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .models import Inspection
from .serializers import CreateInspectionSerializer, InspectionSerializer, MiniInspectionSerializer
from django.http import Http404
from rest_framework.parsers import FormParser, MultiPartParser
from Favorites.models import Favorite_property
from rest_framework.generics import CreateAPIView
import random
from datetime import datetime
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class BookInspection(CreateAPIView):
    serializer_class = CreateInspectionSerializer
    parser_classes = [FormParser, MultiPartParser]

    @staticmethod
    def generate_random_code():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

    def find_unique_random_code(self):
        while True:
            random_code = self.generate_random_code()
            if not Inspection.objects.filter(inspection_id=random_code).exists():
                break
        return random_code

    @staticmethod
    def check_district(properties):
        first_district = properties[0].prop.district.lower()
        for prop in properties[1:]:
            if prop.prop.district.lower() != first_district:
                return False
        return True

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = self.request.user
        properties = [
            validated_data['prop_1'],
            validated_data.get('prop_2'),
            validated_data.get('prop_3')
        ]
        for prop in properties:
            if prop and prop.user != user:
                return Response({'You do not have access to this prorperty'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.check_district([prop for prop in properties if prop]):
            raise ValidationError("Properties are not in the same district")

        inspection_id = self.find_unique_random_code()
        date_created = datetime.now()

        if validated_data['date'].strftime("%Y-%m-%d") < datetime.now().strftime("%Y-%m-%d"):
            return Response({'message': 'Invalid date inputted'}, status=status.HTTP_400_BAD_REQUEST)

        if Inspection.objects.filter(user=user, date=validated_data['date']).exists():
            return Response({'message': 'You cannot book more than one inspection for the same date'}, status=status.HTTP_400_BAD_REQUEST)

        inspection = Inspection.objects.create(
            user=user,
            inspection_id=inspection_id,
            date_created=date_created,
            district=properties.prop.district,
            date=validated_data['date'],
            timeslot=validated_data['timeslot'],
            prop_1=validated_data['prop_1'],
            prop_2=validated_data.get('prop_2'),
            prop_3=validated_data.get('prop_3')
        )

        
        template = render_to_string(
            'main/inspection.html', 
            {
                'user': user, 
                'pid1': validated_data['prop_1'].prop.property_id, 
                'pid2': validated_data['prop_2'].prop.property_id if validated_data.get('prop_2') else None, 
                'pid3': validated_data['prop_3'].prop.property_id if validated_data.get('prop_3') else None, 
                'date': validated_data['date'], 
                'time': validated_data['timeslot'], 
                'inspect': inspection_id 
            }
        )
        email = EmailMessage(
            'New Inspection Booked',
            template,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )
        email.send()

        data = {'message': 'success', 'data': serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)


class GetAllInspections(APIView):
    serializer_class = MiniInspectionSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user 
        try:
            inspect = Inspection.objects.filter(user=user)
        except Inspection.DoesNotExist:
            raise Http404

        serializer = MiniInspectionSerializer(inspect, many=True)
        data = {'message': 'success',
                'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class GetInspection(APIView):
    serializer_class = InspectionSerializer

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user 

        inspect = Inspection.objects.get(id=pk)
        if inspect.user != user:
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = InspectionSerializer(inspect)
        data = {'message': 'success',
                'member_id': inspect.user.member_id,
                'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class GetInspectionwithID(APIView):
    serializer_class = InspectionSerializer

    def get(self, request, inspect_id=None, *args, **kwargs):
        inspect = Inspection.objects.get(inspection_id=inspect_id)

        serializer = InspectionSerializer(inspect)
        data = {'message': 'success',
                'member_id': inspect.user.member_id,
                'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
