from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Docunment(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	identity_card = models.FileField(upload_to='identity_card/', blank=True)
	CAC = models.FileField(upload_to='CAC/', blank=True)

	def __str__(self):
		return self.user.__str__()
