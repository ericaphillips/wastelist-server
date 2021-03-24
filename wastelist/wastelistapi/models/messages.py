from django.db import models

class Message(models.Model):
    sender = models.ForeignKey("WasteUser", on_delete=models.DO_NOTHING, related_name="sender")
    receiver = models.ForeignKey("WasteUser", on_delete=models.DO_NOTHING, related_name="receiver")
    content = models.CharField(max_length=500)