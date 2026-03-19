from django.contrib import admin

from .models import PortfolioProject


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'featured', 'active', 'order', 'created_at']
    search_fields = ['title', 'short_description', 'full_description']
    list_filter = ['featured', 'active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', '-created_at']
