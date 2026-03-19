from rest_framework import serializers

from .models import PortfolioProject


class PortfolioProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProject
        fields = [
            'id',
            'title',
            'slug',
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
