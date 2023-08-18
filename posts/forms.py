from django import forms
from .models import PostComment, Post


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['body',]

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white',
    }))
    class Meta:
        model = Post
        exclude = ['author', 'date_created', 'likes', 'date_updated']

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white',
    }))
    class Meta:
        model = Post
        exclude = ['date_created', 'date_updated', 'author', 'likes']