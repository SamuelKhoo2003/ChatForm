from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.http import HttpResponse
# Create your views here.

# rooms = [
#     {'id':1, 'name':'What is your favourite movie?'},
#     {'id':2, 'name':'Why should I learn to drive?'},
#     {'id':3, 'name':'Is it worth it to invest in Nvidia?'},
# ]

def loginpage(request): 
    page = 'login'
    # we don't want the user to access the login page again if they are already logged in 
    if request.user.is_authenticated: 
        return redirect('home')
    
    # note do not call login, as login is a built in function and calling/name it login may cause clashes 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except: 
            messages.error(request, 'User does not exist')
    # we are making use of django flash messages, which are messages which are stored inside of django and stored in only 1 browser refresh 
        user = authenticate(request, username=username, password=password)
        # this is verifiying whether the user exists

        if user is not None: 
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Username or Password is incorrect, please try again.')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutuser(request): 
    logout(request)
    return redirect ('home')

def registeruser(request): 
    form = UserCreationForm()
    if request.method == "POST": 
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False)
            # we want to be able to access the user right way hence we set commit to False, essentially freezing it in time
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An error occured during registation') 
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)  
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    # a future idea is to add in a follower system where you can filter out the activity to those which you follow
    room_activity = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count, 'room_activity': room_activity}
    return render(request, 'base/homepg.html', context)

def room(request, pk): 
    roomval = Room.objects.get(id=pk)
    room_messages = roomval.message_set.all().order_by('-created')
    # message_set.all means that messages related to the parent owner (in this case room) is called 
    participants = roomval.participants.all()
    if request.method == 'POST': 
        message = Message.objects.create(
            user=request.user,
            room=roomval,
            body=request.POST.get('body')
        )
        roomval.participants.add(request.user)
        # this is a built in add function so then the user will be automatically added to the room they join 
        return redirect('room', pk=roomval.id)
        # note it is "objects" not object and also note that pk is roomval.id not room.id 
        # return redirect('home')
    
    context = {'room': roomval, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/roompg.html', context)


def userprofile(request, pk): 
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_activity = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'topics': topics, 'room_activity': room_activity}
    return render(request, 'base/profile.html', context)




# note the pk in rooms which is also used in urls, we can use pk as an id as it will always be unique
@login_required(login_url="login")
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect ('home')
        
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # if request.user != room.host: 
    #     return HttpResponse('Room host not found')
    # we no longer need this as we have removed the option for the edit and delete button from the front end if the user isnt the host

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url="login")
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host: 
        return HttpResponse('Room host not found')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})



@login_required(login_url="login")
def deletemessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user: 
        return HttpResponse('Message user not found')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url="login")
def updateruser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST': 
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect ('user-profile', pk=user.id)
    return render(request, 'base/update_profile.html', {'form': form})

# another future idea is to have an editting function fo
# @login_required(login_url="login")
# def editmessage(request, pk):
#     message = Message.objects.get(id=pk)

#     if request.user != message.user: 
#         return HttpResponse('Message user not found')
    
#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')
#     return render(request, 'base/room_form.html', {'obj':message})

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    rooms = Room.objects.all()
    return render(request, 'base/topics.html', {'topics':topics, 'rooms': rooms})

def activitiespage(request): 
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {})