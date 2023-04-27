from dataclasses import Field
from os import name
from django.db import models
from django.forms import CharField, DateField, IntegerField
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField('Product Name', max_length=50, default='')
    price = models.IntegerField('Price', default=0)
    """     product_date = models.DateTimeField('Date') """
    description = models.TextField(
        'Description', max_length=1000, null=False, default='')
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL, related_name='products')

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
