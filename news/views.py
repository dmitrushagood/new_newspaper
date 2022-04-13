from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class NewsView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    #form_class = PostForm


class PostView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = 'post'


