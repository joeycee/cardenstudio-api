from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE

from .models import ServiceOffering


TINYMCE_CONFIG = {
    'height': 360,
    'menubar': False,
    'plugins': 'lists link code preview',
    'toolbar': 'undo redo | blocks | bold italic underline | bullist numlist | link | removeformat | code preview',
}


class ServiceOfferingAdminForm(forms.ModelForm):
    short_description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 12}, mce_attrs=TINYMCE_CONFIG)
    )
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 24}, mce_attrs=TINYMCE_CONFIG)
    )

    class Meta:
        model = ServiceOffering
        fields = '__all__'


@admin.register(ServiceOffering)
class ServiceOfferingAdmin(admin.ModelAdmin):
    form = ServiceOfferingAdminForm
    list_display = ['title', 'slug', 'featured', 'active', 'order', 'created_at']
    search_fields = ['title', 'short_description', 'description']
    list_filter = ['featured', 'active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', '-created_at']
