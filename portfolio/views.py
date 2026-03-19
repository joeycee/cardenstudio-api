from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import PortfolioProject
from .serializers import PortfolioProjectSerializer

class PortfolioProjectListView(ListAPIView):
    queryset = PortfolioProject.objects.filter(active=True)
    serializer_class = PortfolioProjectSerializer

class PortfolioProjectDetailView(RetrieveAPIView):
    queryset = PortfolioProject.objects.filter(active=True)
    serializer_class = PortfolioProjectSerializer
    lookup_field = 'slug'
