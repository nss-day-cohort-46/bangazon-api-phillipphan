from django.db import models
from django.db.models.deletion import DO_NOTHING
from bangazonapi.models import Customer, Product

class CustomerLikes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)