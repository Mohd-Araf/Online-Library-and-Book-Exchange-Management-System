from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Registration
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration Successful! Please login.")
            return redirect('login')
    return render(request, 'register.html')

# Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'login.html')

# Dashboard (After Login)
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {"user": request.user})
    else:
        return redirect('login')

# Logout
def logout_user(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render

# Create your views here.
