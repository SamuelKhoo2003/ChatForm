from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#     {'id':1, 'name':'What is your favourite movie?'},
#     {'id':2, 'name':'Why should I learn to drive?'},
#     {'id':3, 'name':'Is it worth it to invest in Nvidia?'},
# ]

def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)  
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/homepg.html', context)

def room(request, pk): 
    roomval = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         roomval = i 
    context = {'room': roomval}
    return render(request, 'base/roompg.html', context)

# note the pk in rooms which is also used in urls, we can use pk as an id as it will always be unique

def createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})