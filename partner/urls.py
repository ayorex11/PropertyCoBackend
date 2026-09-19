from django.urls import path
from . import views
urlpatterns = [
	path('request/', views.PartnerWithUs.as_view()),
]