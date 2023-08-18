from django import forms
from .models import Assignment

class EditForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white'}))
    sinflar = (
        ('', '-------'),
        ('5.1', '5.1'),
        ('5.2', '5.2'),
        ('6.1', '6.1'),
        ('6.2', '6.2'),
        ('7.1', '7.1'),
        ('7.2', '7.2'),
        ('7.3', '7.3'),
        ('8.1', '8.1'),
        ('8.2', '8.2'),
        ('8.3', '8.3'),
        ('9.1', '9.1'),
        ('9.2', '9.2'),
        ('9.3', '9.3'),
        ('10.1', '10.1'),
        ('10.2', '10.2'),
        ('10.3', '10.3'),
        ('11.1', '11.1'),
        ('11.2', '11.2'),
        ('11.3', '11.3'),
    )
    sinf = forms.ChoiceField(choices=sinflar, widget=forms.Select(attrs={'class': 'form-control'}))
    is_readed = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    qachongacha = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control bg-dark text-white', 'type':'datetime-local'}))
    max_ball = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control bg-dark text-white', 'step':'0.00001'}))
    class Meta:
        fields = '__all__'
        model = Assignment