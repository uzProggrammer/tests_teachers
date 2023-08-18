from django import forms
from .models import Problem
from users.models import MyUser
from attempts.models import Attempt

class TaskForm(forms.ModelForm):
    author = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'form-control bg-dark text-white', }
    ), queryset=MyUser.objects.all())
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white',
    }))
    time_limit = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    memory_limit = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    difficulty = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    info_out = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ))
    info_in = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ))
    simple_tests = forms.JSONField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    tests = forms.JSONField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    yechim = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ))
    class Meta:
        model = Problem
        exclude = ['foiz', 'accepteds', 'wrong_answers',]




class TaskEditForm(forms.ModelForm):
    author = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'form-control bg-dark text-white', }
    ), queryset=MyUser.objects.all())
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white',
    }))
    time_limit = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    memory_limit = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    difficulty = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    info_out = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ))
    info_in = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ))

    simple_tests = forms.JSONField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white',
        }, 
    ), required=False)
    tests = forms.JSONField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white',
        }
    ))
    yechim = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control bg-dark text-white for_tiny',
        }
    ),required=False)
    class Meta:
        model = Problem
        exclude = ['foiz', 'accepteds', 'wrong_answers', ]

class AttemptForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea(attrs={'id': 'code-editor'}), label='')
    class Meta:
        model = Attempt
        fields = ['code']