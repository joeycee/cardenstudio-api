from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import ServiceOffering
from .serializers import ServiceOfferingSerializer

class ServiceOfferingListView(ListAPIView):
    queryset = ServiceOffering.objects.filter(active=True)
    serializer_class = ServiceOfferingSerializer

class ServiceOfferingDetailView(RetrieveAPIView):
    queryset = ServiceOffering.objects.filter(active=True)
    serializer_class = ServiceOfferingSerializer
    lookup_field = 'slug'
