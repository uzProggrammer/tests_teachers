from django import forms
from .models import Task,TaskQuestion
from ckeditor.widgets import CKEditorWidget

class TaskCkEditForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(), label='Haqida', help_text='Foydalanuvshiga ko\'rinib turadigan qisim')
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control bg-dark text-white'}
    ), label='Sarlavha', help_text='Siz tuzayotgan testning nomi. Misol uchun: <i>Biologiya 7-sinf</i>')
    ball =forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control bg-dark text-white'}), label='Ball', help_text='Har bir test uchun nechi baldan')
    class Meta:
        model = Task
        fields = ('title', 'about', 'ball',)

class RichTask(forms.ModelForm):
    class Meta:
        fields = ('is_active', )
        model = Task