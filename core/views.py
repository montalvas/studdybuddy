from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    
    return render(request, 'core/home.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        
        user = authenticate(request, username=username, password=password)  
        
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Username OR password doest not match.')  
          
    return render(request, 'core/login_register.html', {'page': 'login'})

def logout_page(request):
    if not request.user.is_authenticated:
        return redirect('core:login')
    
    logout(request)
    return redirect('core:home')

def register_page(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('core:home')
        
        else:
            messages.error('An error had occured during registration.')
    
    return render(request, 'core/login_register.html', {'form': form})

# Rooms

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    return render(request, 'core/room.html', {'room': room})

@login_required(login_url='core:login')
def create_room(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    
    context = {
        'form': form,
        'title': 'Create Room'
        }
    
    return render(request, 'core/form_room.html', context)

@login_required(login_url='core:login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here.")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    
    context = {
        'form': form,
        'title': 'Update Room'
        }
    
    return render(request, 'core/form_room.html', context)

@login_required(login_url='core:login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here.")
    
    if request.method == 'POST':
        room.delete()
        return redirect('core:home')
    
    return render(request, 'core/delete_room.html', {'obj': room})