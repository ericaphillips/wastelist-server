from django.db import models

class PharmacyCustomer(models.Model):
    customer = models.ForeignKey("WasteUser", on_delete=models.DO_NOTHING, related_name="pharmacycustomers")
    pharmacy = models.ForeignKey("Pharmacy", on_delete=models.DO_NOTHING, related_name="pharmacycustomers")