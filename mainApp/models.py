from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

class Product(models.Model):
	name = models.CharField(max_length = 50)
	image = models.CharField(max_length = 100) # shared link
	image_name = models.CharField(max_length = 100)
	description = models.TextField()
	gender = models.IntegerField(default = -1) # 0 men 1 woman 2 both
	price = models.DecimalField(max_digits = 6, decimal_places = 2)
	is_featured = models.IntegerField(default = 0)
	is_transit = models.IntegerField(default = 1) # is in procces of creation 1 yes 0 no

	def __str__(self):
		return self.name


class Profile (models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=30) 

