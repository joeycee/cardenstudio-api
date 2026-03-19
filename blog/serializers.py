from rest_framework import serializers

from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'featured_image',
            'featured',
            'published_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
