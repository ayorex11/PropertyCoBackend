from django.urls import path
from . import views

urlpatterns=[
	path('notifications/',views.get_notifications),
	path('read/<str:pk>/', views.mark_as_read),
	path('agentnotifications/', views.get_my_notifications),
	path('mark_read/<str:pk>/', views.mark_read),

]