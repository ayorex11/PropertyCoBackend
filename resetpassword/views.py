from dj_rest_auth.views import PasswordResetView
from .serializers import CustomPasswordResetSerializer

class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
