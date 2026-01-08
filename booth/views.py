import base64, uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Photo

def home(request):
    return render(request, 'home.html')

# ---------- LOGIN ----------
def login_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('capture')
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})

# ---------- SIGNUP ----------
def signup_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('capture')

    return render(request, 'signup.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def capture(request):
    if request.method == 'POST':
        data = request.POST.get('image')
        format, imgstr = data.split(';base64,')
        img = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.png')
        Photo.objects.create(user=request.user, image=img)
        return redirect('gallery')

    return render(request, 'capture.html')

@login_required
def gallery(request):
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'gallery.html', {'photos': photos})

@login_required
def delete_photo(request, id):
    photo = get_object_or_404(Photo, id=id, user=request.user)
    photo.image.delete()
    photo.delete()
    return redirect('gallery')

@login_required
def delete_all(request):
    photos = Photo.objects.filter(user=request.user)
    for photo in photos:
        photo.image.delete()
        photo.delete()
    return redirect('gallery')
