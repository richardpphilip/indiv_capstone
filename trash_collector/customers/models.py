from django.db import models


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', default=0, on_delete=models.CASCADE)
