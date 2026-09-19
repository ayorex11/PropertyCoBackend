from .models import  Blog
from .serializers import  Blogserializer, miniserializer
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):

	book = Blog.objects.filter(draft=False)
	serializer = miniserializer(book, many=True)

	data ={'message': 'success',
			'data': serializer.data}

	return Response(data=data, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([AllowAny])

def read_blog(request, pk):
	try:
		books = Blog.objects.get(id=pk)
	except Blog.DoesNotExist:
		raise Http404
	
	serializer = Blogserializer(books, many=False)

	data = {'message': 'success',
			'data': serializer.data}

	return Response(data=data, status=status.HTTP_200_OK)




@swagger_auto_schema(methods=["POST"], request_body=Blogserializer())
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def post_blog(request):
	user = request.user 
	serializer = Blogserializer(data=request.data)
	if user.is_admin == False:
		return Response({'message': 'Invalid Request'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer.is_valid(raise_exception=True)
	serializer.save(date_created=datetime.now())
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_201_CREATED) 

@swagger_auto_schema(methods=["POST"], request_body=Blogserializer())
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def post_blog_draft(request):
	user = request.user 
	serializer = Blogserializer(data=request.data)
	if user.is_admin == False:
		return Response({'message': 'Invalid Request'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer.is_valid(raise_exception=True)
	serializer.save(date_created=datetime.now(), draft=True)
	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(methods=["PATCH"], request_body=Blogserializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def update_blog(request, pk):
	user = request.user
	profile = get_object_or_404(Blog, id=pk)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer = Blogserializer(profile, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()

	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete(request, pk):
	user = request.user
	blog = Blog.objects.get(id=pk)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	blog.delete()
	return Response({'message':'success'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def place_in_drafts(request, pk):
	user = request.user
	blog = Blog.objects.get(id=pk)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	if blog.draft == True:
		return Response({'message': 'blog already in drafts'}, status=status.HTTP_400_BAD_REQUEST)

	blog.draft = True
	blog.save()

	return Response({'message': 'blog placed in drafts'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def remove_from_drafts(request, pk):
	user = request.user
	blog = Blog.objects.get(id=pk)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	if blog.draft == False:
		return Response({'message': 'blog not in drafts'}, status=status.HTTP_400_BAD_REQUEST)

	blog.draft = False
	blog.save()

	return Response({'message': 'blog removed from drafts'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])


def get_drafts(request):
	user = request.user
	blog = Blog.objects.filter(draft=True)
	if user.is_admin == False:
		return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
	serializer = miniserializer(blog, many=True)

	data = {'message': 'success',
			'data': serializer.data}

	return Response(data, status=status.HTTP_200_OK)


