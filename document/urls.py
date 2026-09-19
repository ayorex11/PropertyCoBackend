from django.urls import path
from . import views 
urlpatterns=[
	path('upload-doc/', views.upload),
	path('update/', views.update_docunments),
	path('all_docunment/', views.get_all_docunments),
	path('get_my_docunment/', views.get_my_docunment),
    path('get_user_docunment/<str:email_address>/', views.get_user_docunment),
]