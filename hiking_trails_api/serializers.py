from rest_framework import serializers
from .models import HikingTrails


class HikingTrailsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "owner", "trail_name", "description", "lat", "lon", "google_maps_directions", "all_trails_link")
        model = HikingTrails
