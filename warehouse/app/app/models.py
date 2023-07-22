from django.db import models

class Product(models.Model):
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()