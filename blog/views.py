from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListView(ListAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer

class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
