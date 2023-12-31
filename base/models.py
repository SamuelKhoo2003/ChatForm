from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# we use the existing django user model first  
# Create your models here.

class Topic(models.Model):
    #topic can have many rooms while a room can only have 1 topic 
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name 
    
class Room(models.Model): 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # it is important for us to start a related name as we already have user connected to host earlier in this class

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self): 
        return self.name 
    
class Message(models.Model):
    # this is a one to many data relationship, we specificy the attribute and the parent name 
    # a user can have many messages but a message can only have 1 user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #by doing models.cascade it is so that when a room is deleted all the subsequent messages and things within the room are also deleted 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    #the 0:50 means first 50 characters of the message


#by setting null = true in the textfield, it means that the database can have an instance of the model without the description having a value
#blank is also similar to setting null, it allows for the description to be added later not upon creation 
#auto_now = True means that everytime the save method is called we take a time stamp to record the progress and time of changes made, auto_now_add is when the first change is made  
