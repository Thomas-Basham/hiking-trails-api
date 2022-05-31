from rest_framework import generics
from .models import HikingTrails
from .permissions import IsOwnerOrReadOnly
from .serializers import HikingTrailsSerializer


# Create your views here.
class HikingTrailsList(generics.ListCreateAPIView):
    queryset = HikingTrails.objects.all()
    serializer_class = HikingTrailsSerializer


class HikingTrailsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = HikingTrails.objects.all()
    serializer_class = HikingTrailsSerializer
