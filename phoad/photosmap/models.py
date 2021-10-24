from django.db import models

from django.conf import settings


class Photo(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
