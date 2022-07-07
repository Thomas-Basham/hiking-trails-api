from django.contrib.auth import get_user_model
from django.db import models


class HikingTrails(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    trail_name = models.CharField(max_length=64)
    description = models.TextField()
    google_maps_directions = models.URLField(max_length=600)
    all_trails_link = models.URLField(max_length=600)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)

    def __str__(self):
        return self.trail_name

