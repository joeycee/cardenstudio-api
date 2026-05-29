from rest_framework import serializers

from config.seo import absolute_site_url
from .models import PortfolioProject


class PortfolioProjectSerializer(serializers.ModelSerializer):
    seo_title = serializers.CharField(source='effective_seo_title', read_only=True)
    meta_description = serializers.CharField(source='effective_meta_description', read_only=True)
    public_url = serializers.SerializerMethodField()

    def get_public_url(self, obj):
        return absolute_site_url(f'/work/{obj.slug}')

    class Meta:
        model = PortfolioProject
        fields = [
            'id',
            'title',
            'slug',
            'seo_title',
            'meta_description',
            'public_url',
            'short_description',
            'full_description',
            'featured_image',
            'project_url',
            'github_url',
            'featured',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
