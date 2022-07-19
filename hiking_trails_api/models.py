from django.contrib.auth import get_user_model
from django.db import models
from .scraper import scrape_trail_name, scrape_lat_lon, scrape_google_directions
import time
from urllib.parse import urlparse


class HikingTrails(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    trail_name = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    google_maps_directions = models.CharField(max_length=600, blank=True)
    wta_link = models.URLField(max_length=600)
    lat = models.CharField(max_length=100, blank=True)
    lon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.trail_name

    # take the wta link
    def save(self, *args, **kwargs):
        if not self.pk and not self.lat:
            url_string = self.wta_link
            lat_lon = scrape_lat_lon(url_string)
            time.sleep(1)
            self.trail_name = scrape_trail_name(url_string)
            time.sleep(1)
            google_directions = scrape_google_directions(url_string)
            google_directions = urlparse(google_directions)
            self.google_maps_directions = "https://" + google_directions.path
            time.sleep(1)
            self.lat = lat_lon[0]
            self.lon = lat_lon[1]

        super().save(*args, **kwargs)
