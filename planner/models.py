from django.db import models

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    days = models.IntegerField()

    def __str__(self):
        return self.destination