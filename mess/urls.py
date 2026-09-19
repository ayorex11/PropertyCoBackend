from django.urls import path
from . import views 

urlpatterns = [
	path('send_message/', views.UserMessageCreateView.as_view()),
	path('admin_send_message/', views.AdminMessageCreateView.as_view()),
	path('get_messages/', views.GetMessages.as_view()),
	path('UsersGetMessages/', views.UsersGetMessages.as_view()),
	path('AdminGetSentMessages/', views.AdminGetSentMessages.as_view()),
	path('sent_messages/', views.GetSentMessages.as_view()),
	path('read_message/<str:pk>/', views.GetMessageFully.as_view()),
	path('user_read_message/<str:pk>/', views.UserGetMessageFully.as_view()),
	path('user_mark_as_read/<str:pk>/', views.UserReadMessage.as_view()),
	path('mark_as_read/<str:pk>/', views.ReadMessage.as_view()),

]