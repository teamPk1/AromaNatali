from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length = 50)
	#image = сonnect to google drive
	description = models.TextField()
	brand = models.CharField(max_length = 50)
	gender = models.IntegerField(default = -1)
	price = models.DecimalField(max_digits = 6, decimal_places = 2)
	amount_present = models.IntegerField(default = 0)

class Orders(models.Model):
	product_name = models.ForeignKey(Product, default = None, on_delete = models.CASCADE)
	# Deletion of product should be possible only when there's no product in waiting
	user_name = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
	status = models.IntegerField(default = 0) # 0 waiting, 1 sent 2 arrived 3 collected
	
class Review(models.Model):
	product_name = models.ForeignKey(Product, default = None, on_delete = models.CASCADE)
	rate = models.IntegerField()
	review = models.TextField()
	user_name = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
	