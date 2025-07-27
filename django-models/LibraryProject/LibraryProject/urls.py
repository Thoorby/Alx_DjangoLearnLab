from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD:LibraryProject/LibraryProject/urls.py
    path('', include('relationship_app.urls')), 
=======
    path('', include('relationship_app.urls')),
>>>>>>> 490bb1b1b4bc3491b1150b2a192077d7b3e3f17a:LibraryProject/urls.py
]
