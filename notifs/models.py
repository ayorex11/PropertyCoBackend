from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Notification(models.Model):
	title = models.CharField(max_length=250, blank=True, null=True)
	body = models.CharField(max_length=250, blank=True, null=True)
	date_created = models.DateTimeField()
	read = models.BooleanField(default=False)

	def __str__(self):
		return self.title 

	class Meta:
		ordering = ['-date_created',]


class AgentNotification(models.Model):
	user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
	title = models.CharField(max_length=250, blank=True, null=True)
	body = models.CharField(max_length=250, blank=True, null=True)
	date_created = models.DateTimeField()
	read = models.BooleanField(default=False)

	def __str__(self):
		return self.title 

	class Meta:
		ordering = ['-date_created',]