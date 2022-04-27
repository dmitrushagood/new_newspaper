from django.forms import ModelForm, BooleanField, CharField, Textarea, MultipleChoiceField, HiddenInput
from .models import Post, Category
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class PostForm(ModelForm):
    check_box = BooleanField(label='Ало, Галочка!')

    class Meta:
        model = Post
        fields = ['author', 'cats', 'title', 'text', 'check_box']


class BasicSignupForm(SignupForm):  # автоматическое добавление новых юзеров в группу common

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
