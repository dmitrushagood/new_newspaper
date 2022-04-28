from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import post_filter
from django.core.paginator import Paginator
from datetime import datetime
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.mail import send_mail


class NewsView( ListView):
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
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
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
        context['filter'] = post_filter(self.request.GET,
                                        queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # обязателньо сначала миксин, иначе не работает
    model = Post
    template_name = 'news/post_add.html'
    context_object_name = 'post_add'
    form_class = PostForm

    permission_required = ('news.add_post',)

    #permission_required = ('news.add_Post',
    #                       'news.change_Post')


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return redirect('news')

    '''def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        # блок с дополнительным кодом, например, вызов таски celery_notify_subscribers
        return result

Про вопрос добавления нескольких категорий через add, если categorys-список категорий:
    add(*categorys)
    
    Это написала Екатерина 
    '''

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # редактор публикации
    model = Post
    template_name = 'news/post_add.html'
    # context_object_name = 'post_update'
    form_class = PostForm

    permission_required = ('news.add_post',
                           'news.change_post')

    #permission_required = ('news.change_Post',)


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = '/news'


class Upgraded(TemplateView):
    model = Post
    template_name = 'news/upgraded.html'
    #success_url = 'news'


@login_required
def upgrade_me(request):
    user = request.user  # получили объект текущего пользователя из переменной запроса
    author_status = Group.objects.get(name='author')  # Вытащили author_группу из модели Group
    if not request.user.groups.filter(name='author').exists():  # проверяем, находится ли пользователь в этой группе
        # (вдруг кто-то решил перейти по этому URL, уже имея Author статус).
        author_status.user_set.add(user)  # он всё-таки ещё не в ней — добавляем.
    return redirect('/news/upgraded/')


@login_required
def subscribe(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    for cats in post.cats.all():
        user = User.objects.get(pk=request.user.id)
        cats.subscribers.add(user)
    return redirect('news')





# class IndexView(LoginRequiredMixin, TemplateView):
#    template_name = 'protect/index.html'
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
#        return context

