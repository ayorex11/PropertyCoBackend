from django.urls import path
from . import views 
urlpatterns=[
	path('view/', views.get_profile),
	path('update/', views.update_profile),
	path('get_all_agents/', views.get_all_agents),
	path('get_agent_by_email/<str:email>/', views.get_agent_by_email),
	path('update_agent_rating/<str:member_id>/', views.update_agent_rating),
    path('verify_user/<str:member_id>/', views.verify_user),
    path('unverify_user/<str:member_id>/', views.unverify_user),
]