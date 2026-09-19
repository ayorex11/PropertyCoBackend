from django.db import models
from properties.models import Property
from django.contrib.auth import get_user_model

user = get_user_model()

class Favorite_property(models.Model):
	user = models.ForeignKey(user, related_name='user_fave', blank=False, on_delete=models.CASCADE)
	prop = models.ForeignKey(Property, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.prop.__str__()

	class Meta:
		ordering = ['id',]