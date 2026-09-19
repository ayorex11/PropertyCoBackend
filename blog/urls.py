from django.urls import path 
from . import views

urlpatterns = [
	path('blog_list/', views.post_list),
	path('draft_list/', views.get_drafts),
	path('read_blog/<str:pk>/', views.read_blog),
	path('post_blog/', views.post_blog),
	path('post_blog_draft/', views.post_blog_draft),
	path('update_blog/<str:pk>/', views.update_blog),
	path('delete/<str:pk>/', views.delete),
	path('place_in_drafts/<str:pk>/', views.place_in_drafts),
	path('remove_from_drafts/<str:pk>/', views.remove_from_drafts),

]
