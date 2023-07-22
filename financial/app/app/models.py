from django.db import models

class Invoice(models.Model):
    order_id = models.PositiveBigIntegerField()
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=255)