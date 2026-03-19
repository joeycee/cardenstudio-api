from django.db import models


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.business_name or 'Individual'}"

    class Meta:
        ordering = ['-featured', '-created_at']
