from django.urls import path
from . import views

urlpatterns = [
	path('all_history/', views.all_history),
	path('my_history/', views.my_history),
	path('get_history/<email>/', views.get_history),

]