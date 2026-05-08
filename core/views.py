from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return HttpResponse("No file selected")

        # Optional: file size limit (50MB)
        if uploaded_file.size > 50 * 1024 * 1024:
            return HttpResponse("File too large (max 50MB)")

        try:
            obj = File(user=request.user)
            obj.file = uploaded_file   # correct for CloudinaryField
            obj.save()
        except Exception as e:
            return HttpResponse(str(e))

        return redirect('dashboard')

    files = File.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'files': files})


@login_required
def delete_file(request, id):
    file = get_object_or_404(File, id=id, user=request.user)
    file.delete()
    return redirect('dashboard')