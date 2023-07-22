from django.db import models

class Order(models.Model):
    product_id = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()