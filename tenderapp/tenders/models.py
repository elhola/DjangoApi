from django.db import models


class Tender(models.Model):
    tender_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.tender_id
