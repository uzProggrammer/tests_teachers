from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser
# from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    sinflar = (
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
        ('Guest', 'Guest'),
    )
    username = forms.CharField(label='Foydalanuvchi nomi', widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}), help_text='Siz bu yerga faqat alfabitning [A-z] bo\'lgan harflar yoki sonlarni kiritishingiz mumkin!', error_messages={'unique': 'Bu foydalanuvchi nomi allaqachon tizimda'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}), label='Email manzil', help_text='O\'zingizning email manzilingizni kiriting')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white'}), required=False, label='Ism', help_text='O\'zingizning ismingizni yozing')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}), required=False,
                    label='Familya', help_text='O\'zingizning familyangizni yozing')
    sinf = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control bg-dark text-white'}, choices=sinflar,), label='Sinf', help_text='O\'z sinfingizni tanlang', choices=sinflar)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white'}), help_text='Esingizda qoladigan parolni yozing!', label='Parol')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white'}), help_text='Parolni takrorlang', label='Parolni takrorlang')


    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'sinf',]
        model = MyUser

class UserProfile(forms.ModelForm):

    username = forms.CharField(label='Foydalanuvchi nomi',
                               widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
                               help_text='Siz bu yerga faqat alfabitning [A-z] bo\'lgan harflar yoki sonlarni kiritishingiz mumkin!',
                               error_messages={'unique': 'Bu foydalanuvchi nomi allaqachon tizimda'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}),
                             label='Email manzil', help_text='O\'zingizning email manzilingizni kiriting')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
                                 required=False, label='Ism', help_text='O\'zingizning ismingizni yozing')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
                                required=False,
                                label='Familya', help_text='O\'zingizning familyangizni yozing')
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-white'}),
                          help_text='O\'zingiz haqingizda ma\'lumot beirng', label='Haqida')

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', ]
        model = MyUser