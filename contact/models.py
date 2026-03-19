from django.db import models


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    business_name = models.CharField(max_length=100, blank=True)
    project_type = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=50, blank=True)
    timeline = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']
