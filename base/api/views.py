from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# this function shows us all the routes within our API
@api_view(['GET'])
def getroutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms', 
        'GET /api/rooms/:id',
    ]
    return Response(routes)

# we set safe = False as we want to be able to use more than the python dictionary here 
# safe is only needed for JsonReponse 
@api_view(['GET'])
def getrooms(request): 
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    # we set many as true as we are serializing a query set which has multiple objects/pieces of data 
    return Response(rooms)

# we can configure the django-cors-headers to configure which urls will have accss to the api data and etc (this is not done in this instance)