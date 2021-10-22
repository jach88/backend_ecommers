from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarcaSerializer, ProductoSerializer, RegistroSerializer, VentaSerializer
from .models import DetallePedidoModel, MarcaModel, PedidoModel, ProductoModel, UsuarioModel
from cloudinary import CloudinaryImage, CloudinaryVideo
from cloudinary.uploader import upload, destroy
from cloudinary import config
from .utils import PaginacionPersonalizada
from os import environ
from django.db import transaction
from dotenv import load_dotenv

load_dotenv()
# Create your views here.
config(
    cloud_name=environ.get('CLOUD_NAME'),
    api_key=environ.get('API_KEY'),
    api_secret=environ.get('API_SECRET')
)

class RegistroController(CreateAPIView):
    serializer_class = RegistroSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)

        if data.is_valid():
            data.save()
            return Response(data={
                'message': 'Usuario creado exitosamente',
                'content':data.data
            })
        else:
            return Response(data={
                'message': 'Error al crear el usuario',
                'content': data.errors
            })



class MarcasController(ListCreateAPIView):
    serializer_class = MarcaSerializer
    queryset = MarcaModel.objects.all()
    pagination_class = PaginacionPersonalizada
    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'content':data.data,
                'message': 'Marca creado exitosamente'
            },status=201)
        else:
            return Response(data={
                'message': 'Error al crear la Marca',
                'content': data.errors
            }, status=400)

    # def get(self, request: Request):
    #     data = self.serializer_class(instance=self.get_queryset(),many=True)
    #     return Response(data={
    #         'message': None,
    #         'content':data.data
    #     })
class MarcaController(RetrieveUpdateDestroyAPIView):
    serializer_class = MarcaSerializer
    queryset = MarcaModel.objects.all()

    def delete(self, request: Request, id):

        marcaEncontrada = self.get_queryset().filter(marcaId=id).first()

        if not marcaEncontrada:
            return Response(data={
                'message': 'Marca no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            data = marcaEncontrada.delete()
        except Exception as e:

            return Response(data={
                'message': e.args[0]
            },status=403)

        
        return Response(data={
            'message': 'Marca eliminada exitosamente',
            
        })
    def put(self, request: Request, id):
        marcaEncontrada = self.get_queryset().filter(marcaId=id).first()

        if marcaEncontrada is None:
            return Response(data={
                'message': 'Marca no encontrada',
                'content': None
            }, status=status.HTTP_404_NOT_FOUND)
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.update(instance=marcaEncontrada,
                                validated_data=data.validated_data)
            return Response(data={
                "message": "Marca actualizada exitosamente",
                "content": data.data
            })
        else:
            return Response(data={
                "message": "Error al actualizar la marca",
                "content": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductosController(ListCreateAPIView):
    serializer_class = ProductoSerializer
    queryset = ProductoModel.objects.all()
    pagination_class = PaginacionPersonalizada

    def post(self,request: Request):

        rpta :dict = request.data.copy()
        talla = request.data.get('productoTalla')
        listaTalla =  talla.replace(' ','').split(',')
        rpta['productoTalla'] = listaTalla
        idMarca = rpta.get('marca')
        archivo = request.data.get('productoFoto')
        resultado = ""
        objMarca = MarcaModel.objects.filter(marcaId=idMarca).first()
        if objMarca ==None:
            return Response(data={
                'message': 'La marca no existe',
                'content': None
            })

        if archivo:
            if archivo !=None:

                resultado = upload(archivo,resource_type="image")
                rpta['productoFoto']= resultado.get('url')
            else:
                rpta['productoFoto']=''
            
        data = self.serializer_class(data=rpta)
        
        if data.is_valid():
            data.save()
            return Response(data={
                'content': data.data,
                'message': 'Producto creado exitosamente'
            })
        else:
            if resultado:
                destroy(resultado.get('public_id'))
            return Response(data={
                'message': 'Error al crear el producto',
                'content':data.errors
            },status=400)
    # def get(self, request: Request):
    #     data = self.serializer_class(instance=self.get_queryset(),many=True)
    #     return Response(data={
    #         'message': None,
    #         'content':data.data
    #     })

class ProductoController(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductoSerializer
    queryset = ProductoModel.objects.all()

    def delete(self, request: Request, id):
        objDetalle :DetallePedidoModel = DetallePedidoModel.objects.filter(producto=id).first()
        if objDetalle:
            return Response(data={
                'message': 'este producto existe en la tabla Detalle'
            },status=403)
        productoEncontrado :ProductoModel = self.get_queryset().filter(productoId=id).first()
        
        if not productoEncontrado:
            return Response(data={
                'message': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            url =productoEncontrado.__getattribute__('productoFoto')
            if url:
                    
                idFoto = url[-24:]
                idPartition = idFoto.partition('.')
                data = productoEncontrado.delete()
                destroy(idPartition[0])
            elif not url:
                data = productoEncontrado.delete()
        except Exception as e:
            
            return Response(data={
                'message': e.args[0]
            },status=403)

        
        return Response(data={
            'message': 'Producto eliminado exitosamente',
            
        })


    def put(self, request: Request, id):
        productoEncontrado = ProductoModel.objects.filter(
            productoId=id).first()
        
        if productoEncontrado is None:
            return Response(data={
                "message": "Producto no exite",
                "content": None
            }, status=status.HTTP_404_NOT_FOUND)

        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.update(instance=productoEncontrado,
                                validated_data=data.validated_data)
            return Response(data={
                "message": "Pruducto actualizado exitosamente",
                "content": data.data
            })
        else:
            return Response(data={
                "message": "Error al actualizar el producto",
                "content": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # return super().delete(request, *args, **kwargs)
class VentaController(CreateAPIView):
    serializer_class = VentaSerializer

    def post(self, request : Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            cliente_id = data.validated_data.get('cliente_id')
            detalles = data.validated_data.get('detalle')
            try:
                with transaction.atomic():
                    cliente = UsuarioModel.objects.filter(
                        usuarioId=cliente_id).first()

                    if not cliente:
                        raise Exception('Usuario incorrectos')

                    if cliente.usuarioTipo != 3:
                        raise Exception('Cliente no corresponde el tipo')

                    pedido = PedidoModel(
                        pedidoTotal=0, cliente=cliente)

                    pedido.save()
                    for detalle in detalles:
                        producto_id = detalle.get('producto_id')
                        cantidad = detalle.get('cantidad')
                        producto = ProductoModel.objects.filter(
                            productoId=producto_id).first()
                        if not producto:
                            raise Exception('Producto {} no existe'.format(
                                producto_id))
                        if cantidad > producto.productoCantidad:
                            raise Exception(
                                'No hay suficiente cantidad para el producto {}'.format(producto.productoNombre))
                        producto.productoCantidad = producto.productoCantidad - cantidad
                        producto.save()
                        detallePedido = DetallePedidoModel(detalleCantidad=cantidad,
                                                           detalleSubTotal=producto.productoPrecio * cantidad,
                                                           producto=producto,
                                                           pedido=pedido)
                        detallePedido.save()
                        pedido.pedidoTotal += detallePedido.detalleSubTotal
                        pedido.save()
                return Response(data={
                    'message': 'Venta agregada exitosamente'
                })

            except Exception as e:
                return Response(data={
                    'message': e.args
                }, status=400)

        else:
            return Response(data={
                'message': 'Error al agregar la venta',
                'content': data.errors
            })
