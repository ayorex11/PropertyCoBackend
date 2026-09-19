from django.urls import path
from . import views 
urlpatterns=[
	path('favorite/create/', views.FavoritePropertyCreateView.as_view(), name='favorite-create'),
	path('delete/<str:pk>/', views.remove_favorite.as_view()),
	path('get-favorites/', views.get_favorites.as_view()),
]