from django.urls import path
from .views import HikingTrailsDetail, HikingTrailsList

urlpatterns = [
    path("", HikingTrailsList.as_view(), name="hiking_trails_list"),
    path("<int:pk>/", HikingTrailsDetail.as_view(), name="hiking_trails_detail"),
]