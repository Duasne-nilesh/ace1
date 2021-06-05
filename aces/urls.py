from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('calc.urls')),
    path('',include('sub.urls')),
    path('admin/', admin.site.urls),
]
