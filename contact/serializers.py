from rest_framework import serializers

from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    recaptcha_token = serializers.CharField(write_only=True)

    class Meta:
        model = ContactSubmission
        fields = [
            'id',
            'name',
            'email',
            'business_name',
            'project_type',
            'budget_range',
            'timeline',
            'message',
            'recaptcha_token',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
