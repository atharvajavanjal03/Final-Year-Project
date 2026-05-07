from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import File

def signup_view(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if request.method == 'POST':
        f = request.FILES['file']
        File.objects.create(user=request.user, file=f)

    files = File.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'files': files})

def delete_file(request, id):
    file = File.objects.get(id=id)
    file.delete()
    return redirect('dashboard')