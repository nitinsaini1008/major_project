from django.db import models
from django.contrib.auth.models import User

class items(models.Model):
	name=models.CharField(max_length=200)
	price=models.IntegerField()
	quantity=models.IntegerField()
	desc=models.TextField()
	type_of_item=models.CharField(max_length=100)
	photo=models.ImageField(upload_to='itmephotos')
	datetime=models.DateTimeField(auto_now_add=True)


class products(models.Model):
	name=models.CharField(max_length=200)
	desc=models.CharField(max_length=500)
	photo=models.ImageField(upload_to='itmephotos')
	datetime=models.DateTimeField(auto_now_add=True)
	item=models.ManyToManyField(items, null=True, blank=True)

	def total_item(self):
		return self.item.count()
class buyed(models.Model):
	item=models.ForeignKey(items,on_delete=models.CASCADE)
	total_item=models.IntegerField()

class cart(models.Model):
	name=models.ForeignKey(User,on_delete=models.CASCADE, unique=True)
	cost=models.IntegerField(default=0)
	item=models.ManyToManyField(buyed, null=True, blank=True)
	datetime=models.DateTimeField(auto_now_add=True)

class order_count(models.Model):
	item=models.ForeignKey(items,on_delete=models.CASCADE)
	item_count=models.IntegerField(default=0)
class allorder(models.Model):
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	cost=models.IntegerField(default=0)
	datetime=models.DateTimeField(auto_now_add=True)	
	address=models.CharField(max_length=1000)
	item=models.ManyToManyField(order_count, blank=True, null=True)

class re_views(models.Model):
	point=models.IntegerField(default=0)
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(items,on_delete=models.CASCADE)
	datetime=models.DateTimeField(auto_now_add=True)
	msg=models.CharField(max_length=500)