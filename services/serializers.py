from rest_framework import serializers

from .models import ServiceOffering


class ServiceOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOffering
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'description',
            'price_from',
            'featured',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
