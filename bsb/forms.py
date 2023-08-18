from django import forms
from .models import BsbAssignment, BsbProblemAnswer, BsbProblem


class EditForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white'}))
    is_readed = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    ball = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control bg-dark text-white', 'step':'0.00001'}))
    class Meta:
        exclude = ['author', 'is_readed', 'Bsb', 'max_ball',]
        model = BsbAssignment

class AttemptForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'id': 'code-editor'}), label='')
    class Meta:
        model = BsbProblemAnswer
        fields = ['body']