from django.db import models


# Create your models here.
class Position(models.Model):
    user = models.ForeignKey('accounts.User', default=0, on_delete=models.CASCADE)
    selected_ticker = models.CharField(max_length=5, null=True)
    selected_value = models.IntegerField(default=0)
    position_value = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.selected_ticker
