from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarcaSerializer, ProductoSerializer
from .models import MarcaModel, ProductoModel
from cloudinary import CloudinaryImage, CloudinaryVideo
from cloudinary.uploader import upload, destroy
from cloudinary import config
from os import environ
from dotenv import load_dotenv

load_dotenv()
# Create your views here.
config(
    cloud_name=environ.get('CLOUD_NAME'),
    api_key=environ.get('API_KEY'),
    api_secret=environ.get('API_SECRET')
)
class MarcaController(ListCreateAPIView):
    serializer_class = MarcaSerializer
    queryset = MarcaModel.objects.all()

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'content':data.data,
                'message': 'Marca creado exitosamente'
            })
        else:
            return Response(data={
                'message': 'Error al crear la Marca',
                'content': data.errors
            }, status=400)

    def get(self, request: Request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message': None,
            'content':data.data
        })



class ProductosController(ListCreateAPIView):
    serializer_class = ProductoSerializer
    queryset = ProductoModel.objects.all()

    def post(self,request: Request):
        archivo = request.data.get('productoFoto')
        resultado = upload(archivo,resource_type="image")
        rpta: dict = request.data
        rpta['productoFoto']= resultado.get('url')
        rpta['productoTalla'] = ["1","2"]
        data = self.serializer_class(data=rpta)
        
        if data.is_valid():
            data.save()
            return Response(data={
                 'content': data.data,
                'message': 'Producto creado exitosamente'
            })
        else:
            destroy(resultado.get('public_id'))
            return Response(data={
                'message': 'Error al crear el producto',
                'content':data.errors
            })
    def get(self, request: Request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message': None,
            'content':data.data
        })

class ProductoController(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductoSerializer
    queryset = ProductoModel.objects.all()

    def delete(self, request: Request, id):
        
        productoEncontrado = self.get_queryset().filter(productoId=id).first()
        
        if not productoEncontrado:
            return Response(data={
                'message': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            data = productoEncontrado.delete()
        except Exception as e:
            print(e)

        # data = PlatoModel.objects.filter(platoId=id).delete()
        # (num_registros_eliminados, { platoModel: id })
        return Response(data={
            'message': 'Producto eliminado exitosamente'
        })
        # return super().delete(request, *args, **kwargs)