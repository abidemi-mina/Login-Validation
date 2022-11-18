from django.shortcuts import render
from .forms import *

# Create your views here.
# 
def home(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def register(request):
    register = RegisterForm()
    if request.method == 'POST':
        register = RegisterForm(request.POST)
        if register.is_valid():
            user = register.save()
            user.refresh_from_db()
            user.profile.first_name = register.cleaned_data.get('first_name')
            user.profile.last_name = register.cleaned_data.get('last_name')
            user.profile.email = register.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()

    return render(request,'register.html')
