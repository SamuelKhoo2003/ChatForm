from django.db import models

# Create your models here.

class Room(models.Model): 
    #host = 
    #topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name 
    
    
#by setting null = true in the textfield, it means that the database can have an instance of the model without the description having a value
#blank is also similar to setting null, it allows for the description to be added later not upon creation 
#auto_now = True means that everytime the save method is called we take a time stamp to record the progress and time of changes made, auto_now_add is when the first change is made  
