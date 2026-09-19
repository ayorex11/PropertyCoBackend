from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Request(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cat = (
		('Rent', 'Rent'),
		('Sale', 'Sale'),
		('Joint Venture', 'Joint Venture'),
		)
	category = models.CharField(max_length=50, blank=False, choices=cat, default = 'Rent')
	property_type=(
		('Detached Bungalows', 'Detached Bungalows'),
		('Semi-Detached Bungalows', 'Semi-Detached Bungalows'),
		('Terraced Bungalows', 'Terraced Bungalows'),
		('Flat/Apartment','Flat/Apartment'),
		('Detached Duplexes', 'Detached Duplexes'),
		('Semi-Detached Duplexes', 'Semi-Detached Duplexes'),
		('Terraced Duplexes', 'Terraced Duplexes'),
		('Land', 'Land'),
		('Shops', 'Shops'),
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
	beds = models.IntegerField(blank=True)
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
	district = models.CharField(max_length=200, choices=distro, default='', blank=True)
	description = models.CharField(max_length=2500, blank=True)
	budget = models.DecimalField(max_digits=15, decimal_places=2)
	payment_opt = (
		('6 months', '6 months'),
		('12 months', '12 months'),
		('18 months', '18 months'),
		('24 months', '24 months'),
		('36 months', '36 months'),
		('48 months', '48 months'),
	)
	payment_plan = models.CharField(max_length=200, choices=payment_opt, blank=True, null=True)