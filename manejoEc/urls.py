from django.urls import path
from .views import (MarcaController, ProductoController, ProductosController)

urlpatterns = [
    path('marca',MarcaController.as_view()),
    path('productos',ProductosController.as_view()),
    path('producto/<int:id>',ProductoController.as_view()),
]