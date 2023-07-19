from django.db import models

class Order(models.Model):
    productId = models.PositiveBigIntegerField() # TODO relationship
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()