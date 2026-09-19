from django.urls import path
from . import views 
urlpatterns=[
    path('my-catalogue/', views.view_catalogue.as_view()),
    path('view_unapproved_catalogue/', views.view_unapproved_catalogue.as_view()),
    path('view_disapproved_catalogue/', views.view_disapproved_catalogue.as_view()),
    path('remove/<str:pk>/',views.remove.as_view()),
    path('edit-property/<str:pk>/', views.EditProperty.as_view()),
    path('under-contract/<str:pk>/', views.UnderContract.as_view()),
    path('repost/<str:pk>/', views.RepostProperty.as_view()),
]