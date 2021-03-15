from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=75)
    address = models.CharField(max_length=500)
    zipcode = models.IntegerField()
    appointment_hours = models.CharField(max_length=200)