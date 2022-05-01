from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserCreationForm, UpdateUserForm
from .my_func import check_email

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages}
    
    return render(request, 'core/home.html', context)

################### User ########################

def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    messages = user.message_set.all()
    
    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'room_messages': messages
    }
    
    return render(request, 'core/profile.html', context)

@login_required(login_url='core:login')
def update_profile(request):
    user = request.user
    form = UpdateUserForm(instance = user)
    
    if request.method == 'POST':  
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:profile', pk=user.id)
    
    return render(request, 'core/update-user.html', {'form': form})

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
            messages.error(request, 'An error had occured during registration.')
    
    return render(request, 'core/login_register.html', {'form': form})

################### Rooms ########################

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        
        room.participants.add(request.user)
        
        return redirect('core:room', pk=room.id)
    
    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants}
    
    return render(request, 'core/room.html', context)

@login_required(login_url='core:login')
def create_room(request):
    form = RoomForm()
    
    topics = Topic.objects.all()
    title = 'Create Room'
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),  
        )
        
        return redirect('core:home')
    
    context = {'form': form, 'topics': topics, 'title': title}
    
    return render(request, 'core/form_room.html', context)

@login_required(login_url='core:login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    topics = Topic.objects.all()
    title = 'Update Room'
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here.")
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        
        room.save()
        
        return redirect('core:home')
    
    context = {'form': form, 'topics': topics, 'title': title}
    
    return render(request, 'core/form_room.html', context)

@login_required(login_url='core:login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here.")
    
    if request.method == 'POST':
        room.delete()
        return redirect('core:home')
    
    return render(request, 'core/delete.html', {'obj': room})

################### Message ########################

@login_required(login_url='core:login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here.")
    
    if request.method == 'POST':
        message.delete()
        return redirect('core:home')
    
    return render(request, 'core/delete.html', {'obj': message})