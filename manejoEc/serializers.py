from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from manejoEc.models import MarcaModel, ProductoModel, UsuarioModel


class RegistroSerializer(serializers.ModelSerializer):

     # forma 1 => declarar el atributo modificando sus validaciones a nivel de modelo y poniendo nuevas validaciones
    # password = serializers.CharField(write_only=True, required=True)
    def save(self):
        usuarioNombre = self.validated_data.get('usuarioNombre')
        usuarioApellido = self.validated_data.get('usuarioApellido')
        usuarioTipo = self.validated_data.get('usuarioTipo')
        usuarioDni = self.validated_data.get('usuarioDni')
        usuarioCorreo = self.validated_data.get('usuarioCorreo')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(usuarioNombre=usuarioNombre,usuarioApellido=usuarioApellido,
        usuarioTipo=usuarioTipo,usuarioDni=usuarioDni,usuarioCorreo=usuarioCorreo)
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()

        return nuevoUsuario
    class Meta:
        model = UsuarioModel
        # fields = '__all__'
        exclude = ['groups','user_permissions','is_superuser','last_login','is_active','is_staff']

        extra_kwargs ={
            'password':{
                'write_only':True
            }
        }

class MarcaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarcaModel
        
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # productoTalla = serializers.CharField(max_length=2)

    class Meta:
        model = ProductoModel

        # fields = ('productoNombre','productoPrecio','marca','productoTalla')
        fields = ('__all__')
        
class DetalleVentaSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(required=True)
    producto_id = serializers.IntegerField(required=True)


class VentaSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(min_value=0, required=True)
    detalle = DetalleVentaSerializer(many=True, required=True)