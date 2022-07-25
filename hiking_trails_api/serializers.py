from rest_framework import serializers
from .models import HikingTrails


class HikingTrailsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "owner", "trail_name", "description", "lat", "lon", "google_maps_directions", "wta_link")
        model = HikingTrails
