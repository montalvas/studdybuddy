from django.shortcuts import render
from .models import Room

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request, 'core/home.html', {'rooms': rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    return render(request, 'core/room.html', {'room': room})