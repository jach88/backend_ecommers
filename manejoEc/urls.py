from django.urls import path
from .views import (MarcaController, MarcasController, ProductoController, ProductosController, RegistroController, VentaController)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('login',TokenObtainPairView.as_view()),
    path('refresh-session',TokenRefreshView.as_view()),
    path('registro',RegistroController.as_view()),
    path('marcas',MarcasController.as_view()),
    path('marca/<int:id>',MarcaController.as_view()),
    path('productos',ProductosController.as_view()),
    path('producto/<int:id>',ProductoController.as_view()),
    path('generar-compra',VentaController.as_view())
]