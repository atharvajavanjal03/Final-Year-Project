from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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


@login_required
def dashboard(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        new_file = File(user=request.user)
        new_file.file = uploaded_file   # ✅ correct for Cloudinary
        new_file.save()                 # ✅ required step

        return redirect('dashboard')

    files = File.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'files': files})


@login_required
def delete_file(request, id):
    file = File.objects.get(id=id)
    file.delete()
    return redirect('dashboard')