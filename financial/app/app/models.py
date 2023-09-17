from django.db import models

class Invoice(models.Model):
    class StatusChoices(models.TextChoices):
        INCOMPLETE = 'incomplete', 'Incomplete'
        WAITING = 'waiting', 'Waiting'
        COMPLETE = 'complete', 'Complete'

    order_id = models.PositiveBigIntegerField(unique=True)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=StatusChoices.choices)

    def save(self, *args, **kwargs):
        if self.status not in self.StatusChoices.values:
            raise ValueError(f"Invalid status: {self.status}")
        super().save(*args, **kwargs)