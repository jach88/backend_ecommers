from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manejoEc/',include('manejoEc.urls')),
    path('facturacion/', include('facturacion.urls')),
]
