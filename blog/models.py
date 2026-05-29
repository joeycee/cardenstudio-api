from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def effective_seo_title(self):
        return self.seo_title or self.title

    @property
    def effective_meta_description(self):
        return self.meta_description or self.excerpt

    class Meta:
        ordering = ['-published_at', '-created_at']
