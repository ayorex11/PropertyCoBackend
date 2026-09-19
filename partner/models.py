from django.db import models
class Partner(models.Model):
	first_name = models.CharField(max_length=500, blank=False)
	last_name = models.CharField(max_length=500, blank=True)
	phone_number = models.CharField(max_length=20, blank=False)
	email = models.CharField(max_length=500, blank=False)

	def __str__(self):
		return self.first_name