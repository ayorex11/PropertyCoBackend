from django.urls import path
from . import views
urlpatterns = [
	path('request/', views.RequestProperty.as_view()),
]