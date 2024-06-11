from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class WordFrom(forms.Form):
    word = forms.CharField()

class UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['word', 'openai_key']
