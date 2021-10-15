from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from manejoEc.models import MarcaModel, ProductoModel

class MarcaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarcaModel

        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # productoTalla = serializers.CharField(max_length=2)

    class Meta:
        model = ProductoModel

        # fields = ('productoNombre','productoPrecio')
        fields = ('__all__')

