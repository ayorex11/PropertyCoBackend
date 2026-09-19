from django.urls import path
from . import views 
urlpatterns=[
	path('properties/', views.get_properties.as_view()),
	path('get_unapproved_properties/', views.get_unapproved_properties.as_view()),
	path('get_disapproved_properties/', views.get_disapproved_properties.as_view()),
	path('get_properties_by_property_co/', views.get_properties_by_property_co.as_view()),
	path('search/', views.search_properties.as_view()),
	path('featured/', views.featured_properties.as_view()),
	path('lagos/', views.lagos_properties.as_view()),
	path('abuja/', views.abuja_properties.as_view()),
	path('ogun/', views.ogun_properties.as_view()),
	path('PH/', views.port_harcourt_properties.as_view()),
	path('get_property/<str:pk>/', views.view_property.as_view()),
	path('property_id/<str:prop_id>/', views.reference_search.as_view()),
	path('search_rent_prop/', views.search_rent_properties.as_view()),
	path('search_sale_prop/', views.search_sale_properties.as_view()),
	path('search_jointventure_prop/', views.search_Joint_Venture_properties.as_view()),
	path('post-property/', views.PostProperty.as_view()),
	path('make-featured/<str:pk>/', views.MakeFeatured.as_view()),
	path('RemoveFeatured/<str:pk>/', views.RemoveFeatured.as_view()),
	path('ApproveProperty/<str:pk>/', views.ApproveProperty.as_view()),
	path('DisapproveProperty/<str:pk>/<str:reason>/', views.DisapproveProperty.as_view()),
	path('DeleteProperty/<str:pk>/', views.DeleteProperty.as_view()),


]