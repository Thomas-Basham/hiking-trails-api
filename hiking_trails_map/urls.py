from django.urls import path
from .views import HikingTrailsMapView

urlpatterns = [
    path('', HikingTrailsMapView.as_view(), name='hiking_trails_map'),
]