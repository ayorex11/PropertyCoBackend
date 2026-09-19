from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class History(models.Model):
	user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
	rating = models.CharField(max_length=200, blank=False)
	reason = models.CharField(max_length=250, blank=True, null=True)
	date = models.DateTimeField()

	def __str__(self):
		return self.user.__str__()