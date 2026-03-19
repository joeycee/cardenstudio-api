from django.db import models
from django.utils.text import slugify


class PortfolioProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    full_description = models.TextField()
    featured_image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while PortfolioProject.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']
