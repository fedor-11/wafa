from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('mapp/', include('mapp.urls')),
    path('admin/', admin.site.urls),
]
