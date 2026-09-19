from django.urls import path
from . import views 
urlpatterns=[
	path('view/', views.get_profile),
	path('update/', views.update_profile),
	path('get_non_agents/', views.get_non_agents),
	path('get_non_agents_email/<str:email>/', views.get_non_agents_email),
]