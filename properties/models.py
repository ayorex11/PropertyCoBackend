from django.db import models
from django.contrib.auth import get_user_model
from Agents.models import Profile
class Property(models.Model):
	name = models.CharField(max_length=200, blank=False)
	agent = models.ForeignKey(Profile, blank=False, on_delete=models.CASCADE)
	picture1 = models.ImageField(upload_to='Properties', blank=False)
	picture2 = models.ImageField(upload_to='Properties', blank=False)
	picture3 = models.ImageField(upload_to='Properties', blank=False)
	picture4 = models.ImageField(upload_to='Properties', blank=False)
	picture5 = models.ImageField(upload_to='Properties', blank=True)
	picture6 = models.ImageField(upload_to='Properties', blank=True)
	picture7 = models.ImageField(upload_to='Properties', blank=True)
	picture8 = models.ImageField(upload_to='Properties', blank=True)
	picture9 = models.ImageField(upload_to='Properties', blank=True)
	picture10 = models.ImageField(upload_to='Properties', blank=True)
	beds = models.IntegerField(blank=True, null=True)
	bathrooms = models.IntegerField(blank=True)
	toilets = models.IntegerField(blank=True)
	property_id = models.CharField(max_length=20, blank=False, unique=True)
	description = models.TextField(max_length=5000, blank=True)
	proposal = models.TextField(max_length=5000, blank=True)
	premium = models.TextField(max_length=5000, blank=True)
	sharing_ratio = models.TextField(max_length=5000, blank=True)
	facilitator_fee = models.TextField(max_length=5000, blank=True)
	more_details = models.CharField(max_length=1000, blank=True)
	plac = (
		('Lagos', 'Lagos'),
		('Abuja', 'Abuja'),
		('Ogun', 'Ogun'), 
		('Port Harcourt', 'Port Harcourt'),
		)
	location = models.CharField(max_length=50, choices=plac, default='Lagos')
	places = (
		('Lagos Island', 'Lagos Island'),
		('Lagos Mainland', 'Lagos Mainland'),
		)
	sub_location = models.CharField(max_length=50, choices=places, default='Lagos Island')
	distro = (
		('Lagos Island', 'Lagos Island'),
		('Ikoyi', 'Ikoyi'),
		('VI', 'VI'),
		('Lekki Phase1/Ikate', 'Lekki Phase1/Ikate'),
		('Jakande/Agungi/Chevron', 'Jakande/Agungi/Chevron'),
		('Orchid/Ikota/VGC', 'Orchid/Ikota/VGC'),
		('Ajah', 'Ajah'),
		('Sangotedo', 'Sangotedo'),
		('Abijo/Ibeju Lekki', 'Abijo/Ibeju Lekki'),
		('Epe', 'Epe'),
		('Apapa', 'Apapa'),
		('Agege', 'Agege'),
		('Alimosho/Ipaja', 'Alimosho/Ipaja'),
		('Abule Egba/Agbado', 'Abule Egba/Agbado'),
		('Ikeja', 'Ikeja'),
		('Ogba/Ojodu/Berger', 'Ogba/Ojodu/Berger'),
		('Magodo/Isheri/Arepo', 'Magodo/Isheri/Arepo'),
		('Ojota/Ogudu', 'Ojota/Ogudu'),
		('Maryland-Jibowu', 'Maryland-Jibowu'),
		('Gbagada/Bariga/Somolu', 'Gbagada/Bariga/Somolu'),
		('Yaba/Ebute Meta/Oyingbo', 'Yaba/Ebute Meta/Oyingbo'),
		('Surulere/Iganmu', 'Surulere/Iganmu'),
		('Oshodi/Isolo', 'Oshodi/Isolo'),
		('Ojo/Mile 2/Mebamu', 'Ojo/Mile 2/Mebamu'),
		('Ijaniki/Agbara', 'Ijaniki/Agbara'),
		('Badagry/Araromi', 'Badagry/Araromi'),
		('Ketu/Mile 12', 'Ketu/Mile 12'),
		('Ikorodu', 'Ikorodu'),
		('Sango Ota', 'Sango Ota'),

		)
	district = models.CharField(max_length=200, choices=distro, default='', blank=True, null=True)
	address = models.CharField(max_length=500, blank=False)
	cat = (
		('Rent', 'Rent'),
		('Sale', 'Sale'),
		('Joint Venture', 'Joint Venture'),
		)
	category = models.CharField(max_length=50, blank=False, choices=cat, default = 'Rent')
	property_type=(
		('Detached Bungalow', 'Detached Bungalow'),
		('Semi-Detached Bungalow', 'Semi-Detached Bungalow'),
		('Terrace Bungalow', 'Terrace Bungalow'),
		('Flat/Apartment','Flat/Apartment'),
		('Detached Duplex', 'Detached Duplex'),
		('Semi-Detached Duplex', 'Semi-Detached Duplex'),
		('Terrace Duplex', 'Terrace Duplex'),
		('Residential Land', 'Residential Land'),
		('Commercial Land', 'Commercial Land'),
		('Mixed-Use Land', 'Mixed-Use Land'),
		('Shop', 'Shop'),
		('Office Space', 'Office Space'),
		('WareHouse', 'WareHouse'),
		('Factory', 'Factory'),
		('Complex', 'Complex'),
		('Filling Station', 'Filling Station'),
		('Tank Farm', 'Tank Farm'),
		('Hotel', 'Hotel'),
		('School', 'School'),
		('Church', 'Church'),
		('Hostel', 'Hostel'),
		('Restaurant', 'Restaurant'),
		)
	prop_type = models.CharField(max_length=50,  blank=False, choices=property_type, default='Bungalow')
	price = models.DecimalField(max_digits=15, decimal_places=2)
	ask = (
		('Asking Price', 'Asking Price'),
		('Slightly Negotiable', 'Slightly Negotiable'),
		('Net Price', 'Net Price'),
		('Best Price', 'Best Price'),
		('Per Annum', 'Per Annum'),
		('Per Month', 'Per Month'),
		('Per Square Meter', 'Per Square Meter'),
	)
	price_options = models.CharField(max_length=50, choices=ask, default='Asking Price')
	furnished = models.BooleanField(default=False, blank=True)
	newly_built = models.BooleanField(default=False, blank=True)
	car_park = models.BooleanField(default=False, blank=True)
	shared = models.BooleanField(default=False, blank=True)
	swimming_pool = models.BooleanField(default=False, blank=True)
	gym = models.BooleanField(default=False, blank=True)
	electricity = models.BooleanField(default=False, blank=True)
	created_at = models.DateField()
	updated_at = models.DateField(blank=True, null=True)
	under_contract = models.BooleanField(default=False, blank=True)
	off_plan = models.BooleanField(default=False, blank=True)
	featured = models.BooleanField(default=False, blank=True)
	serviced = models.BooleanField(default=False, blank=True, null=True)
	inside_an_estate = models.BooleanField(default=False, blank=True, null=True)
	payment_opt = (
		('6 months', '6 months'),
		('12 months', '12 months'),
		('18 months', '18 months'),
		('24 months', '24 months'),
		('36 months', '36 months'),
		('48 months', '48 months'),
	)
	payment_options = models.CharField(max_length=200, choices=payment_opt, blank=True, null=True)
	initial_deposit = models.CharField(max_length=200, blank=True, null=True)
	video_available_on_request = models.BooleanField(default=False, blank=True)
	other_amenities = models.TextField(max_length=5000, blank=True)
	approved = models.BooleanField(default=False)
	disapproved = models.BooleanField(default=False)
	def __str__(self):
		return self.name 

	class Meta:
		ordering = ['-agent__rating', '-created_at']


