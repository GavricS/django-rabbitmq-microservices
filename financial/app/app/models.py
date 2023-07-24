from django.db import models

class Invoice(models.Model):
    order_id = models.PositiveBigIntegerField(unique=True)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=255)# TODO status value see https://docs.djangoproject.com/en/4.2/ref/models/fields/#enumeration-types