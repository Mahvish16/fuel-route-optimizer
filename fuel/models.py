from django.db import models

# Create your models here.

class FuelStation(models.Model):
    opis_truckstop_id = models.CharField(max_length=100, blank=True, null=True)
    truckstop_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    rack_id = models.CharField(max_length=100, blank=True, null=True)
    retail_price = models.FloatField()

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"