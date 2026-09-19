from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from properties.models import Property
from properties.serializers import MiniPropSerializer, PropertySerializer, PropSerializer, CreatePropSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from django.http import Http404
from Agents.models import Profile
from rest_framework.parsers import FormParser, MultiPartParser
from datetime import datetime
from notifs.models import Notification


class view_catalogue(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_classes = PropSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        prof = Profile.objects.get(user=user)
        if prof is None:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prop = Property.objects.filter(agent=prof, approved=True)
        except Property.DoesNotExist:
            raise Http404
        serializer = PropSerializer(prop, many=True)
        data = {'message': 'Success',
                'data': serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)


class view_unapproved_catalogue(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_classes = PropSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        prof = Profile.objects.get(user=user)
        if prof is None:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prop = Property.objects.filter(agent=prof, approved=False, disapproved=False)
        except Property.DoesNotExist:
            raise Http404
        serializer = PropSerializer(prop, many=True)
        data = {'message': 'Success',
                'data': serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)

class view_disapproved_catalogue(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_classes = PropSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        prof = Profile.objects.get(user=user)
        if prof is None:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prop = Property.objects.filter(agent=prof, approved=False, disapproved=True)
        except Property.DoesNotExist:
            raise Http404
        serializer = PropSerializer(prop, many=True)
        data = {'message': 'Success',
                'data': serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)


class remove(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request,pk, *args, **kwargs):
        user = self.request.user
        prop = Property.objects.get(id=pk)
        prof= Profile.objects.get(user=user)
        if prop.agent != prof:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        prop.delete()
        return Response({"message": "Success"}, status=status.HTTP_204_NO_CONTENT)


class EditProperty(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreatePropSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = Property.objects.all()
    

    def update(self, request, pk, *args, **kwargs):
        user = self.request.user
        prop = get_object_or_404(Property, id=pk)
        prof = Profile.objects.get(user=user)
        if prop.agent != prof:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreatePropSerializer(prop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            prop.updated_at=datetime.now().strftime("%Y-%m-%d")
            prop.approved = False
            prop.disapproved = False
            prop.save()
            title = 'Property has been edited. Please Review.'
            body = f'Property with id {prop.property_id} has been edited. Please Review if it will be approved or not.'
            date_created = datetime.now()
            read = False
            notif = Notification(title=title, body=body, date_created=date_created, read=read)
            notif.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnderContract(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        prop = get_object_or_404(Property, id=pk)
        prof = Profile.objects.get(user=user)
        if prop.agent != prof:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        if prop.under_contract == True:
            prop.under_contract = False
            prop.save()
            title = 'Property has been removed from Under Contract'
            body = f'Property with id {prop.property_id} has been removed from under contract status'
            date_created = datetime.now()
            read = False
            notif = Notification(title=title, body=body, date_created=date_created, read=read)
            notif.save()
            return Response({'message': 'property has been removed from under contract'}, status=status.HTTP_200_OK)
        prop.under_contract = True
        prop.save()
        title = 'Property has been placed Under Contract'
        body = f'Property with id {prop.property_id} has been placed under contract'
        date_created = datetime.now()
        read = False
        notif = Notification(title=title, body=body, date_created=date_created, read=read)
        notif.save()
        return Response({"message": "Placed under contract"}, status=status.HTTP_200_OK)

class RepostProperty(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        prop = get_object_or_404(Property, id=pk)
        prof = Profile.objects.get(user=user)
        if prop.agent != prof:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        prop.created_at=datetime.now().strftime("%Y-%m-%d")
        prop.save()  # Save any changes required for reposting
        return Response({"message": "Property Reposted"}, status=status.HTTP_200_OK)