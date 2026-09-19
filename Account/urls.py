from django.urls import path
from . import views 
urlpatterns=[
	path('get_all_users/', views.get_all_users),
	path('get_user_by_email/<str:email>/', views.get_user_by_email),
	path('get_all_agents/', views.get_all_agents),
	path('get_all_nonagents/', views.get_all_nonagents),
	path('get_user_by_member_id/<str:member_id>/', views.get_user_by_member_id),

]