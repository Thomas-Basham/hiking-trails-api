from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView
from django_pandas.io import read_frame

from hiking_trails_api.models import HikingTrails
import folium
from folium.plugins import MarkerCluster


import os
import pandas as pd

# Create your views here.
class HikingTrailsMapView(ListView):
    template_name = 'hiking_trails_map.html'
    model = HikingTrails


def maps(request):
    df = read_frame(HikingTrails.objects.all())

    print(df)

    map = folium.Map(width="100%" , max_width="80%", max_height="80%",
                   zoom_start=7)  # if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster, add to m

    marker_cluster = MarkerCluster().add_to(map)
    for i, r in df.iterrows():
        html = f'''
        <h2 >{r["trail_name"].capitalize()}<h2/>
        <a style="color:blue" href="{r["google_maps_directions"]}" target="_blank">Directions via Googlemaps <a/>
        <br>
        <a style="color:green" href="{r["all_trails_link"]}" target="_blank">Link to All-Trails site<a/>
        <p >{r["description"]}<p/>

        '''

        iframe = folium.IFrame(html, width=200, height='300')
        popup = folium.Popup(iframe, max_width=200)

        location = (r["lat"], r["lon"])

        folium.Marker(location=location, tooltip=r["trail_name"].capitalize(), popup=popup).add_to(
            marker_cluster)


    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)
    map = map._repr_html_()
    context = {
        'map': map,
    }

    return render(request, 'hiking_trails_map.html', context)


