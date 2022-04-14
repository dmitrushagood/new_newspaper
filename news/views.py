from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .filters import post_filter
from django.core.paginator import Paginator
from datetime import datetime
from .forms import PostForm


class NewsView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context


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
        # наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = post_filter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context


class PostCreate(CreateView):
    model = Post
    template_name = 'news/post_add.html'
    context_object_name = 'post_add'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return redirect('news')