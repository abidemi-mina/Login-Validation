from email import message
from django.conf import settings
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
# 
def home(request):
    return render(request,'index.html')

def login_page(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
                if user.is_superuser == True :
                    login(request, user)
                    return redirect('home')
                elif not(user.is_superuser):
                    login(request,user)
                    return redirect('home')
         else:
               messages.error(request, 'Email and Password do not match')
    return render(request,'login.html')

def register(request):
    register_form= RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user = register_form.save()
            login(request,user)
            return redirect('login')
        else:
            messages.error(request,'User not registered')
    return render(request,'register.html',{'form':register_form})



    
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "reset-mail.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    plain_message = strip_tags(email)
                    send = send_mail(subject, plain_message,settings.FROM_HOST, [user.email,], html_message=email, fail_silently=False)
                    if send:
                        print(send)
                        messages.success(request, 'Email sent succesfully!')
                        return redirect ("/password_reset/done/")
                    else:
                        print('not sent ')
                        messages.error(request, 'Mail not sent!')
    password_reset_form = PasswordResetForm()
    return render(request, "password-reset.html", {"form":password_reset_form})



