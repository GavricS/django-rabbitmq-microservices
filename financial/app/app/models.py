from django.db import models

class Invoice(models.Model):
    class StatusChoices(models.TextChoices):
        INCOMPLETE = 'incomplete', 'Incomplete'
        WAITING = 'waiting', 'Waiting'
        COMPLETE = 'complete', 'Complete'

    order_id = models.PositiveBigIntegerField(unique=True)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.INCOMPLETE)