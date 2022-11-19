import email
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'enter a valid email'}))

    class Meta():
        model = User
        fields = ('username','password1', 'password2','email')

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exist')
        return email_field

    def clean_username(self):
        name_field = self.cleaned_data.get('username')
        if User.objects.filter(username=name_field).exists():
            raise forms.ValidationError('Name already exist')
        return name_field
    


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()
            return user