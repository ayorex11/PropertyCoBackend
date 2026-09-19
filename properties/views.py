from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Property
from .serializers import MiniPropSerializer, PropertySerializer, PropSerializer, CreatePropSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from django.http import Http404
from Agents.models import Profile
from rest_framework.parsers import FormParser, MultiPartParser
from Account.models import User


from datetime import timedelta, date

class get_properties(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MiniPropSerializer

    def get(self, request, *args, **kwargs):
        thirty_days_ago = date.today() - timedelta(days=30)
        
        prop = Property.objects.filter(
            under_contract=False,
            created_at__gte=thirty_days_ago,
            approved=True
        )

        serializers = PropSerializer(prop, many=True)
        data = {
            'message': 'success',
            'data': serializers.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

class get_properties_by_property_co(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = MiniPropSerializer

	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=24)
		prof = Profile.objects.get(user=user)
		prop = Property.objects.filter(agent=prof)
		serializers = PropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data': serializers.data
		}
		return Response(data=data, status=status.HTTP_200_OK)



from django.db.models import Q

class search_properties(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        prop_type = request.query_params.get('prop_type', None)
        district1 = request.query_params.get('district1', None)
        district2 = request.query_params.get('district2', None)
        district3 = request.query_params.get('district3', None)
        beds = request.query_params.get('beds', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        serviced = request.query_params.get('serviced', None)
        inside_an_estate = request.query_params.get('inside_an_estate', None)

        thirty_days_ago = date.today() - timedelta(days=30)

        query = Q(under_contract=False, approved=True, created_at__gte=thirty_days_ago)


        if prop_type:
            query &= Q(prop_type=prop_type)

        if district1:
            query &= Q(district=district1)

        if district2:
            query &= Q(district=district2)

        if district3:
            query &= Q(district=district3)

        if beds:
            query &= Q(beds=beds)

        if min_price and max_price:
            query &= Q(price__range=(min_price, max_price))

        if serviced:
            query &= Q(serviced=serviced)

        if inside_an_estate:
            query &= Q(inside_an_estate=inside_an_estate)

        prop = Property.objects.filter(query)

        if not prop.exists():
            return Response(data={'message': 'Properties not found for given criteria'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropSerializer(prop, many=True)

        data = {
            'message': 'search successful',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_200_OK)

class featured_properties(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = MiniPropSerializer
	def get(self,request):
		thirty_days_ago = date.today() - timedelta(days=30)
		prop = Property.objects.filter(featured=True, under_contract = False, created_at__gte=thirty_days_ago, approved=True)
		serializer = MiniPropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data': serializer.data
		}
		return Response(data=data, status=status.HTTP_200_OK)

class lagos_properties(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = PropSerializer
	def get(self,request):
		thirty_days_ago = date.today() - timedelta(days=30)
		prop = Property.objects.filter(location='Lagos', under_contract = False, created_at__gte=thirty_days_ago, approved=True)
		serializer = PropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data':serializer.data
		}
		return Response(data=data, status=status.HTTP_200_OK)

class abuja_properties(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = PropSerializer
	def get(self,request):
		thirty_days_ago = date.today() - timedelta(days=30)
		prop = Property.objects.filter(location='Abuja', under_contract = False, created_at__gte=thirty_days_ago, approved=True)
		serializer = PropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data':serializer.data
		}
		return Response(data=data, status=status.HTTP_200_OK)

class ogun_properties(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = PropSerializer
	def get(self,request):
		thirty_days_ago = date.today() - timedelta(days=30)
		prop = Property.objects.filter(location='Ogun', under_contract = False, created_at__gte=thirty_days_ago, approved=True)
		serializer = PropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data':serializer.data
		}
		return Response(data=data, status=status.HTTP_200_OK)

class port_harcourt_properties(APIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = PropSerializer
	def get(self,request):
		thirty_days_ago = date.today() - timedelta(days=30)
		prop = Property.objects.filter(location='Port Harcourt', under_contract = False, created_at__gte=thirty_days_ago, approved=True)
		serializer = PropSerializer(prop, many=True)
		data = {
			'message':'success',
			'data':serializer.data
		}
		return Response(data=data, status=status.HTTP_200_OK)

class view_property(APIView):
	permission_classes = (permissions.AllowAny,) 
	serializer_class = PropertySerializer
	def get(self,request, pk):
		try:
			prop = Property.objects.get(id=pk)
		except Property.DoesNotExist:
			raise Http404
		serializer = PropertySerializer(prop, many=False)
		agent = prop.agent
		agent_data = {}
		agent_data['agent_picture'] = agent.profile_picture.url if agent.profile_picture else None
		agent_data['agent_name'] = "PropertyCo"
		agent_data['agent_number'] = "080X XXX XXXX"

		data = {'message':'success',
				'data':serializer.data,
				'agent_data': agent_data}
		return Response(data=data, status=status.HTTP_200_OK)



class reference_search(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MiniPropSerializer

    def get(self, request, prop_id=None, *args, **kwargs):
        try:
            prop = Property.objects.get(property_id=prop_id) 
            serializer = PropSerializer(prop) 

            data = {
                'message': 'success',
                'data': serializer.data
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Property.DoesNotExist:
            return Response(data={'message': 'Property not found for given criteria'}, status=status.HTTP_404_NOT_FOUND)



class search_rent_properties(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        prop_type = request.query_params.get('prop_type', None)
        district1 = request.query_params.get('district1', None)
        district2 = request.query_params.get('district2', None)
        district3 = request.query_params.get('district3', None)
        beds = request.query_params.get('beds', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        serviced = request.query_params.get('serviced', None)
        inside_an_estate = request.query_params.get('inside_an_estate', None)

        thirty_days_ago = date.today() - timedelta(days=30)

        query = Q(under_contract=False, approved=True, category='Rent', created_at__gte=thirty_days_ago)


        if prop_type:
            query &= Q(prop_type=prop_type)

        if district1:
            query &= Q(district=district1)

        if district2:
            query &= Q(district=district2)

        if district3:
            query &= Q(district=district3)

        if beds:
            query &= Q(beds=beds)

        if min_price and max_price:
            query &= Q(price__range=(min_price, max_price))

        if serviced:
            query &= Q(serviced=serviced)

        if inside_an_estate:
            query &= Q(inside_an_estate=inside_an_estate)

        prop = Property.objects.filter(query)

        if not prop.exists():
            return Response(data={'message': 'Properties not found for given criteria'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropSerializer(prop, many=True)

        data = {
            'message': 'search successful',
            'data': serializer.data
        }



class search_sale_properties(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        prop_type = request.query_params.get('prop_type', None)
        district1 = request.query_params.get('district1', None)
        district2 = request.query_params.get('district2', None)
        district3 = request.query_params.get('district3', None)
        beds = request.query_params.get('beds', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        serviced = request.query_params.get('serviced', None)
        inside_an_estate = request.query_params.get('inside_an_estate', None)

        thirty_days_ago = date.today() - timedelta(days=30)

        query = Q(under_contract=False, approved=True, category='Sale', created_at__gte=thirty_days_ago)


        if prop_type:
            query &= Q(prop_type=prop_type)

        if district1:
            query &= Q(district=district1)

        if district2:
            query &= Q(district=district2)

        if district3:
            query &= Q(district=district3)

        if beds:
            query &= Q(beds=beds)

        if min_price and max_price:
            query &= Q(price__range=(min_price, max_price))

        if serviced:
            query &= Q(serviced=serviced)

        if inside_an_estate:
            query &= Q(inside_an_estate=inside_an_estate)

        prop = Property.objects.filter(query)

        if not prop.exists():
            return Response(data={'message': 'Properties not found for given criteria'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropSerializer(prop, many=True)

        data = {
            'message': 'search successful',
            'data': serializer.data
        }


class search_Joint_Venture_properties(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        prop_type = request.query_params.get('prop_type', None)
        district1 = request.query_params.get('district1', None)
        district2 = request.query_params.get('district2', None)
        district3 = request.query_params.get('district3', None)
        beds = request.query_params.get('beds', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        serviced = request.query_params.get('serviced', None)
        inside_an_estate = request.query_params.get('inside_an_estate', None)

        thirty_days_ago = date.today() - timedelta(days=30)

        query = Q(under_contract=False, approved=True, category='Joint Venture', created_at__gte=thirty_days_ago)

        if prop_type:
            query &= Q(prop_type=prop_type)

        if district1:
            query &= Q(district=district1)

        if district2:
            query &= Q(district=district2)

        if district3:
            query &= Q(district=district3)

        if beds:
            query &= Q(beds=beds)

        if min_price and max_price:
            query &= Q(price__range=(min_price, max_price))

        if serviced:
            query &= Q(serviced=serviced)

        if inside_an_estate:
            query &= Q(inside_an_estate=inside_an_estate)

        prop = Property.objects.filter(query)

        if not prop.exists():
            return Response(data={'message': 'Properties not found for given criteria'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropSerializer(prop, many=True)

        data = {
            'message': 'search successful',
            'data': serializer.data
        }


from rest_framework.generics import CreateAPIView
import random
from datetime import datetime
from django.db import transaction

import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from notifs.models import Notification, AgentNotification


class PostProperty(CreateAPIView):
    serializer_class = CreatePropSerializer
    parser_classes = [FormParser, MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data from serializer
        validated_data = serializer.validated_data

        # Add additional fields
        user = self.request.user
        created_at = datetime.now().strftime("%Y-%m-%d")
        agent = Profile.objects.get(user=user)
        if agent is None:
            return Response({'message': 'users cant create properties'}, status=status.HTTP_400_BAD_REQUEST)

        if agent.verified == False:
            return Response({'message': 'unverified users cannot create properties'}, status=status.HTTP_400_BAD_REQUEST)
        property_id = self.find_unique_random_code()
        if user.is_admin == True:
            approved = True
        else:
            approved = False

        NFA = "NFA"
        pictures = ['picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'picture6', 'picture7', 'picture8', 'picture9', 'picture10']
        for picture_field in pictures:
            picture = validated_data.get(picture_field)
            if picture:
                watermarked_image = self.add_watermark_to_image(picture, property_id, NFA)
                # Overwrite the picture field in validated data with the watermarked image
                validated_data[picture_field] = self.save_watermarked_image(watermarked_image, picture.name)

        # Update serializer with modified validated_data
        properties = Property(property_id=property_id, created_at=created_at, agent=agent, approved=approved, **validated_data)
        properties.save()
        title = 'New Property Posted'
        body = f'User {user} has posted a new property with id {property_id}.'
        date_created = datetime.now()
        read = False
        notif = Notification(title=title, body=body, date_created=date_created, read=read)
        notif.save()
        data = {'message': 'success', 'data': serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)

    def add_watermark_to_image(self, picture, property_id, NFA):
        with Image.open(picture) as img:
            img = img.resize((278, 314), Image.LANCZOS)
            draw = ImageDraw.Draw(img)
            width, height = img.size
            logo_path = 'template/main/trans2.png'
            logo = Image.open(logo_path)
            FONT_COLOR = '#909095'
            logo_width, logo_height = logo.size
            target_logo_width = int(width * 0.2)
            target_logo_height = int(logo_height * target_logo_width / logo_width)
            logo = logo.resize((target_logo_width, target_logo_height))

            logo_margin = 20
            logo_position = (width - target_logo_width - logo_margin, height - target_logo_height - 60)
            img.paste(logo, logo_position, logo)
            font_size = int(min(width, height) * 0.04)
            font = ImageFont.truetype(r'font/Mulish-ExtraBold.ttf', font_size)

            font_siz = int(min(width, height)* 0.08)
            font2 = ImageFont.truetype(r'font/Mulish-ExtraBold.ttf', font_siz)

            # Use textbbox instead of textsize for property_id text
            bbox = draw.textbbox((0, 0), property_id, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            margin = 50
            position = (width - text_width - 40, height - text_height - margin)
            draw.text(position, property_id, fill=FONT_COLOR, font=font)

            # Use textbbox instead of textsize for NFA text
            nfa_bbox = draw.textbbox((0, 0), NFA, font=font2)
            nfa_text_width = nfa_bbox[2] - nfa_bbox[0]
            nfa_text_height = nfa_bbox[3] - nfa_bbox[1]
            nfa_position = ((width - nfa_text_width) // 2, (height - nfa_text_height) // 2)
            draw.text(nfa_position, NFA, fill=FONT_COLOR, font=font2)

            return img

    def save_watermarked_image(self, image, original_filename):
        temp_buffer = BytesIO()
        image.save(temp_buffer, format='JPEG', quality=100)
        temp_buffer.seek(0)

        # Create InMemoryUploadedFile for the watermarked image
        file_name, file_extension = os.path.splitext(original_filename)
        watermarked_image = InMemoryUploadedFile(temp_buffer, None, f'{file_name}_watermarked{file_extension}', 'image/jpeg', temp_buffer.tell(), None)
        return watermarked_image

    # Other methods remain the same...

    def find_unique_random_code(self):
        while True:
            random_code = self.generate_random_code()
            if not Property.objects.filter(property_id=random_code).exists():
                break  # Exit the loop if the code is not in use

        return random_code

    def generate_random_code(self):
        # Predetermined letters
        letters = "PC"

        # Generate random numbers (not more than 4)
        random_numbers = [str(random.randint(0, 4)) for _ in range(2)]

        # Concatenate letters and random numbers
        random_code = letters + ''.join(random_numbers)

        return random_code




class MakeFeatured(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, pk=None, *args, **kwargs):
		user = self.request.user 
		prop = get_object_or_404(Property, id=pk)
		if user.is_admin  == False:
			return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

		if prop.featured == True:
			return Response ({'message':'Property already featured'}, status=status.HTTP_400_BAD_REQUEST)

		prop.featured = True
		prop.save()

		return Response({'message':'success'}, status=status.HTTP_200_OK)

		
class RemoveFeatured(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, pk=None, *args, **kwargs):
		user = self.request.user 
		prop = get_object_or_404(Property, id=pk)
		if user.is_admin  == False:
			return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

		if prop.featured == False:
			return Response ({'message':'Property is not featured'}, status=status.HTTP_400_BAD_REQUEST)

		prop.featured = False
		prop.save()

		return Response({'message':'success'}, status=status.HTTP_200_OK)

class ApproveProperty(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, pk, *args, **kwargs):
		user = self.request.user
		prop = get_object_or_404(Property, id=pk)
		if user.is_admin == False:
			return Response({'message: Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

		prop.approved = True
		prop.disapproved = False
		prop.save()
		User = prop.agent.user
		title = f'Your posted property has been approved' 
		body = f'Your posted property with id {prop.property_id} has been approved'
		date_created = datetime.now()
		read = False
		notif = AgentNotification(user=user, title=title, body=body, date_created=date_created, read=read)
		notif.save()
		data = {'message': 'success',}
		return Response(data=data, status=status.HTTP_200_OK)

class get_unapproved_properties(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MiniPropSerializer

    def get(self, request, *args, **kwargs):
    	user = self.request.user
    	thirty_days_ago = date.today() - timedelta(days=30)

    	prop = Property.objects.filter(
    		created_at__gte=thirty_days_ago,
    		approved=False,
    		disapproved=False,

    		)
    	if user.is_admin == False:
    		return Response({'message: Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    	serializers = PropSerializer(prop, many=True)
    	data = {
    		'message': 'success',
    		'data': serializers.data

    	}	
    	return Response (data=data , status=status.HTTP_200_OK)


class get_disapproved_properties(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MiniPropSerializer

    def get(self, request, *args, **kwargs):
    	user = self.request.user
    	thirty_days_ago = date.today() - timedelta(days=30)

    	prop = Property.objects.filter(
    		created_at__gte=thirty_days_ago,
    		approved=False,
    		disapproved=True,

    		)
    	if user.is_admin == False:
    		return Response({'message: Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    	serializers = PropSerializer(prop, many=True)
    	data = {
    		'message': 'success',
    		'data': serializers.data

    	}	
    	return Response (data=data , status=status.HTTP_200_OK)

class DisapproveProperty(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, reason, *args, **kwargs):
        user = self.request.user
        prop = get_object_or_404(Property, id=pk)
        User = prop.agent.user
        pid = prop.property_id
        if user.is_admin == False:
            return Response({'message: Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        prop.approved = False
        prop.disapproved = True
        prop.save()
        title = f'Your posted property has been disapproved' 
        body = f'Your posted property with id {pid} has been disapproved. Reason: {reason}'
        date_created = datetime.now()
        read = False
        notif = AgentNotification(user=User, title=title, body=body, date_created=date_created, read=read)
        notif.save()
        data = {'message': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)


class DeleteProperty(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	def delete(self, request, pk, *args, **kwargs):
		user = self.request.user
		prop = get_object_or_404(Property, id=pk)
		User = prop.agent.user 
		pid = prop.property_id
		if user.is_admin == False:
			return Response({'message: Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

		prop.delete()
		title = f'Your posted property has been deleted by the admin'
		body = f'Your property with id {pid} has been deleted because it does not follow the rules and guidlines of PropertyCo'
		date_created = datetime.now()
		read = False
		notif = AgentNotification(user=User, title=title, body=body, date_created=date_created, read=read)
		notif.save()
		data = {'message': 'success'}
		return Response(data=data, status=status.HTTP_200_OK)
