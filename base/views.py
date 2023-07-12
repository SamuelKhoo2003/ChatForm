from django.shortcuts import render

# Create your views here.
def home(request): 
    return render(request, 'homepg.html')

def room(request): 
    return render(request, 'roompg.html')
