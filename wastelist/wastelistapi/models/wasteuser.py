from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class WasteUser(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    phone = models.IntegerField()
    zipcode = models.IntegerField()
    pharmacy = models.ForeignKey("Pharmacy", on_delete=CASCADE, null = True)