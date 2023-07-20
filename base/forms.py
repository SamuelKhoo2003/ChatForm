from django.forms import ModelForm
from .models import Room 

# this is how we create a form using the model form that is pre made 

class RoomForm(ModelForm): 
    class Meta: 
        model = Room 
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm): 
    class Meta: 
        model = ['username', 'email']