from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=75)
    address = models.CharField(max_length=500)
    zipcode = models.IntegerField()
    appointment_hours = models.CharField(max_length=200)

    @property
    def customers(self):
            return self.__customers

    @customers.setter
    def customers(self, value):
            self.__customers = value 