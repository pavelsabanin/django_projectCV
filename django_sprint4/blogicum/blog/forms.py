from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'},
                                        format='%Y-%m-%dT%H:%M'),
        }
        exclude = ('author',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
