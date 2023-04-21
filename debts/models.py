from django.db import models
from django.forms import ModelForm

class Money(models.Model):
    payer = models.CharField(max_length = 100)
    payee = models.CharField(max_length = 100)
    sum = models.PositiveIntegerField()
    date = models.DateTimeField("date sent")
    note = models.CharField(max_length = 240)

    class Meta:
        permissions = (("add payment", "add a new payment and edit its data, except the payer"),)