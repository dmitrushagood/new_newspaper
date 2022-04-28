# from django.db.models import Sum
# from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group

from django.db.models import Q, Sum
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_a = self.post_set.all().aggregate(Sum("rating"))
        comment_a = self.user.comment_set.all().aggregate(Sum("rating"))
        comment_to_a = Comment.objects.filter((Q(post__author=self.pk)) & ~Q(user=self.user)).aggregate(Sum("rating"))
        res = list(map(lambda x, y, z: x * 3 + y + z, post_a.values(), comment_a.values(), comment_to_a.values()))[0]
        self.rating = res
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User,  through='CategoryUser')


class CategoryUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    article = 'a'
    news = 'n'

    POST_TYPE = [
        (article, "Статья"),
        (news, "Новость")
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE, default=article)
    created = models.DateTimeField(auto_now_add=True)
    cats = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            pre_text = self.text[:124] + "..."
            return pre_text
        else:
            return self.text

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{Post.objects.get(pk=self.post)} -  {Category.objects.get(pk=self.category)}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
