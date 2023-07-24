from django.contrib import admin
from django.urls import include, path 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), 
    path('api/', include('base.api.urls'))
    # this means any url that starts with api after the home url is redirected to base.api.urls
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
