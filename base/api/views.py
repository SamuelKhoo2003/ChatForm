from django.http import JsonResponse


# this function shows us all the routes within our API
def getroutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms', 
        'GET /api/rooms/:id',
    ]
    return JsonResponse(routes, safe=False)

# we set safe = False as we want to be able to use more than the python dictionary here 