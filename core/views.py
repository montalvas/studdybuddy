from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request, 'core/home.html', {'rooms': rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    return render(request, 'core/room.html', {'room': room})

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

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
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

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('core:home')
    
    return render(request, 'core/delete_room.html', {'obj': room})