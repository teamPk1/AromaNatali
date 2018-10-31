from django.db import models
from django.contrib.auth.models import user

# Create your models here.
class Product(models.Model):
	class Meta_1():
		db_table = "Product"
	name = models.CharField(max_length = 200)
	#image = models.ImageField(uploat_to = 'product_image', blank=True)
	image = models.TextField()
	description = models.TextField()
	drand = models.TextField()
	type1 = models.TextField()
	price = models.FloatField()
	amount_present = models.IntegerField()

class Waiting(models.Model):
	class Meta_2():
		db_table = "Waiting"
	product_name = models.ForeignKey(name,default = None)
	user_name = models.ForeignKey(user,default = None)
	status = models.TextField()
	
class Review(models.Model):
	class Meta_3():
		db_table = "Review"
	product_name = models.ForeignKey(name,default = None)
	rate = models.IntegerField()
	review = models.TextField()
	user_name = models.ForeignKey(user,default = None)
	