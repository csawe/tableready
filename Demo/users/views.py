
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from .forms import NewUserForm
from .models import NewUser

from main.models import Message
# Create your views here.

def user_signup(request):
    form = NewUserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = NewUser.objects.get(username=username)
            user.is_active = True
            user.save()
            one = Message(message_number=1, message_text="", user=user)
            two = Message(message_number=2, message_text="", user=user)
            one.save()
            two.save()
            messages.success(request, "User registration successfull.")
            return redirect("../../")
        else:
            messages.error(request, "Enter valid details")
    context = {
        'form' : form,
    }
    return render(request, 'users/signup.html', context)

def user_login(request):  
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(username=uname, password=pwd)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {uname}')
                return redirect('../../')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, 'Enter valid details')
    form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'Users/login.html', context)

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('../../')