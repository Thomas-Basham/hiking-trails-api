from django.views.generic import ListView
from hiking_trails_api.models import HikingTrails


# Create your views here.
class HikingTrailsMapView(ListView):
    template_name = 'hiking_trails_map.html'
    model = HikingTrails
