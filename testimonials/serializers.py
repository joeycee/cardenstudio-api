from rest_framework import serializers

from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id',
            'client_name',
            'business_name',
            'role',
            'quote',
            'rating',
            'featured',
            'client_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
