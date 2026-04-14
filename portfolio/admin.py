from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE

from .models import PortfolioProject


TINYMCE_CONFIG = {
    'height': 360,
    'menubar': False,
    'plugins': 'lists link code preview',
    'toolbar': 'undo redo | blocks | bold italic underline | bullist numlist | link | removeformat | code preview',
}


class PortfolioProjectAdminForm(forms.ModelForm):
    short_description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 12}, mce_attrs=TINYMCE_CONFIG)
    )
    full_description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 24}, mce_attrs=TINYMCE_CONFIG)
    )

    class Meta:
        model = PortfolioProject
        fields = '__all__'


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    form = PortfolioProjectAdminForm
    list_display = ['title', 'slug', 'featured', 'active', 'order', 'created_at']
    search_fields = ['title', 'short_description', 'full_description']
    list_filter = ['featured', 'active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', '-created_at']
