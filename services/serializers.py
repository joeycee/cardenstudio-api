from rest_framework import serializers

from config.seo import absolute_site_url
from .models import ServiceOffering


class ServiceOfferingSerializer(serializers.ModelSerializer):
    seo_title = serializers.CharField(source='effective_seo_title', read_only=True)
    meta_description = serializers.CharField(source='effective_meta_description', read_only=True)
    public_url = serializers.SerializerMethodField()

    def get_public_url(self, obj):
        return absolute_site_url(f'/offerings#{obj.slug}')

    class Meta:
        model = ServiceOffering
        fields = [
            'id',
            'title',
            'slug',
            'seo_title',
            'meta_description',
            'public_url',
            'short_description',
            'description',
            'price_from',
            'featured',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
