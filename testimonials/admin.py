from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'business_name', 'role', 'rating', 'featured', 'active', 'created_at']
    search_fields = ['client_name', 'business_name', 'quote']
    list_filter = ['featured', 'active', 'rating']
    ordering = ['-featured', '-created_at']
