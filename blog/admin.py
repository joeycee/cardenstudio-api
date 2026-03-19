from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE

from .models import BlogPost


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'slug', 'published', 'featured', 'published_at', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    list_filter = ['published', 'featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_at', '-created_at']
