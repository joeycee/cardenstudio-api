from django.urls import path
from .views import ServiceOfferingListView, ServiceOfferingDetailView

urlpatterns = [
    path('', ServiceOfferingListView.as_view(), name='service-list'),
    path('<slug:slug>/', ServiceOfferingDetailView.as_view(), name='service-detail'),
]