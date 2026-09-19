# myapp/urls.py

from django.urls import path, re_path
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('auth/password/reset/', CustomPasswordResetView.as_view(), name='rest_password_reset'),
    re_path(r'^auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # other urls...
]
