from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id':1, 'name':'What is your favourite movie?'},
    {'id':2, 'name':'Why should I learn to drive?'},
    {'id':3, 'name':'Is it worth it to invest in Nvidia?'},
]

def home(request): 
    context = {'rooms':rooms}
    return render(request, 'base/homepg.html', context)

def room(request, pk): 
    roomval = None
    for i in rooms:
        if i['id'] == int(pk):
            roomval = i 
    context = {'room': roomval}
    return render(request, 'base/roompg.html', context)

# note the pk in rooms which is also used in urls
