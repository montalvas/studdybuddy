from django.shortcuts import render

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Javascript'},
    {'id': 3, 'name': 'Kotlin'}
]

def home(request):
    return render(request, 'core/home.html', {'rooms': rooms})

def room(request, pk):
    room = None
    
    for r in rooms:
        if r['id'] == int(pk):
            room = r
    context = {'room': room}
    
    return render(request, 'core/room.html', context)