from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property
User = get_user_model()

class Message(models.Model):
	sender = models.ForeignKey(User, blank=False, null=False, related_name='message_sender', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, blank=False, null=False,related_name='message_receiver', on_delete=models.CASCADE)
	prop = models.ForeignKey(Property, blank=True, null=True, on_delete=models.SET_NULL)
	property_id = models.CharField(max_length=20, blank=True, null=True)
	subject = models.CharField(max_length=250, blank=False, default="Requested Property")
	body = models.CharField(max_length=5000, blank=False, default="Type your message here")
	read = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.subject

	class Meta:
		ordering = ['-date_created']





class AdminMessage(models.Model):
	sender = models.ForeignKey(User, blank=False, null=False, related_name='adminmessage_sender', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, blank=False, null=False,related_name='adminmessage_receiver', on_delete=models.CASCADE)
	subject = models.CharField(max_length=250, blank=False, default="Requested Property")
	body = models.CharField(max_length=5000, blank=False, default="Type your message here")
	read = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.subject

	class Meta:
		ordering = ['-date_created']