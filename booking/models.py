from django.db import models
from Favorites.models import Favorite_property
from django.contrib.auth import get_user_model
User = get_user_model()
class Inspection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	inspection_id = models.CharField(max_length=6, blank=False, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	district = models.CharField(max_length=300, blank=False)
	date = models.DateField(auto_now_add=False, blank=False)
	time = (
		('8am-12pm', '8am-12pm'),
		('1pm-5pm', '1pm-5pm'),
	)
	timeslot = models.CharField(max_length=50, choices=time, default='9am-12pm')
	prop_1 = models.ForeignKey(Favorite_property, blank=True, null=True, on_delete=models.SET_NULL, related_name='prop_1')
	prop_2 = models.ForeignKey(Favorite_property, blank=True, null=True, on_delete=models.SET_NULL, related_name='prop_2')
	prop_3 = models.ForeignKey(Favorite_property, blank=True, null=True, on_delete=models.SET_NULL, related_name='prop_3')

	def __str__(self):
		return self.user.__str__()



