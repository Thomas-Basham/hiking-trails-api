from django.urls import path
from .views import HikingTrailsMapView, maps

urlpatterns = [
    path('', maps, name='maps'),
]