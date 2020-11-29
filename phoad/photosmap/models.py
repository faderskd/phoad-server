from django.db import models


# Create your models here.
class Photo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()