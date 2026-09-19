from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=250, blank=True)
	last_name = models.CharField(max_length=250, blank=True)
	contact_number = models.CharField(max_length=20, blank=True)
	profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
	email_address = models.EmailField(blank=True, null=True)
	member_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
	verified = models.BooleanField(default=False)
	address = models.CharField(max_length=500, blank=True)
	created_at = models.DateField(auto_now_add=True, null=True )


	def __str__(self):
		return self.user.__str__()

