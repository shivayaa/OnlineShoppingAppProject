from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Category(models.Model):
    cname=models.CharField(max_length=100)

    def __str__(s):
        return s.cname 

class Product(models.Model):
    pname=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.TextField(max_length=300)
    pimage=models.ImageField(upload_to='media',default="")

    category=models.ForeignKey(Category,on_delete=models.CASCADE)

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 

class Order(models.Model):
    totalBill=models.IntegerField()
    orderDate=models.DateField(auto_now=True)
    status=models.CharField(max_length=30,default="Processing")
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class MyImage(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(max_length=300)
    img=models.ImageField(upload_to="media",default="")


