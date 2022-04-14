from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from .filters import post_filter
from django.core.paginator import Paginator

class NewsView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    #form_class = PostForm


class PostView(DetailView):
    model = Post
    template_name = "news/post_detail.html"
    context_object_name = 'post'

class NewsFilter(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'post_filter'
    paginate_by = 4

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у
        # наследуемого класса (привет, полиморфизм)
        context = super().get_context_data(**kwargs)
        context['filter'] = post_filter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context
