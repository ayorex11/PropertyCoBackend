# myapp/serializers.py

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()

class CustomPasswordResetSerializer(PasswordResetSerializer):

    def get_users(self, email):
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)
        if not active_users.exists():
            raise ValidationError(_('No active user found with this email address'))
        return active_users

    def save(self):
        request = self.context.get('request')
        # Get user
        email = self.data['email']
        active_users = self.get_users(email)
        
        for user in active_users:
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Prepare email context
            domain = settings.BASE_URL
            site_name = 'PropertyCo'
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uidb64': uid,
                'user': user,
                'token': token,
                'protocol': 'www',
            }
            
            # Render email content
            subject = 'Password Reset Requested'
            email_template_name = 'main/custom_password_reset_email.html'
            email_content = render_to_string(email_template_name, context)
            
            # Send email
            send_mail(
                subject,
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
