from .models import Post
from django_filters import FilterSet


class post_filter(FilterSet):
    class Meta:
        model = Post
        fields = {'created': ['gt'],
                  'title': ['icontains'],
                  'author': ['exact'],
                  }
