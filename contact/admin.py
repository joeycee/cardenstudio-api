from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project_type', 'handled', 'created_at']
    search_fields = ['name', 'email', 'business_name', 'message']
    list_filter = ['handled', 'project_type']
    ordering = ['-created_at']
