from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView
from hiking_trails_api.models import HikingTrails
import folium
import os


# Create your views here.
class HikingTrailsMapView(ListView):
    template_name = 'hiking_trails_map.html'
    model = HikingTrails


def maps(request):
    coordenadas = list(HikingTrails.objects.values_list('lat','lon'))[-1]

    map = folium.Map(coordenadas)
    folium.Marker(coordenadas).add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)

    map = map._repr_html_()

    context = {
        'map': map,
    }
    return render(request, 'hiking_trails_map.html', context)
