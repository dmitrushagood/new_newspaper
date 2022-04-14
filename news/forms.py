from django.forms import ModelForm, BooleanField, CharField, Textarea, MultipleChoiceField, HiddenInput
from .models import Post, Category
from django.utils.translation import gettext_lazy as _


class PostForm(ModelForm):
    check_box = BooleanField(label='Ало, Галочка!')

    class Meta:
        model = Post
        fields = ['author', 'cats', 'title', 'text', 'check_box']

