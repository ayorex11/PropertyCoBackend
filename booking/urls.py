from django.urls import path
from . import views
urlpatterns=[
	path('BookInspection/', views.BookInspection.as_view()),
	path('GetAllInspections/', views.GetAllInspections.as_view()),
	path('GetInspection/<str:pk>/', views.GetInspection.as_view()),
	path('GetInspectionwithID/<str:inspect_id>/', views.GetInspectionwithID.as_view()),
]