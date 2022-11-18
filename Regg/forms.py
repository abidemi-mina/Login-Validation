import email
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'full_name'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'id':'password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'id':'confirm_password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id':'your_email'}))

    class Meta():
        model = User
        fields = ('username','password1', 'password2','email')

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exist')
        return email_field


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            return user