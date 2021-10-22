from rest_framework.test import APITestCase
from .models import MarcaModel, ProductoModel


class MarcasTestCase(APITestCase):

    def setUp(self):
        MarcaModel(marcaNombre='nike',
                    marcaDescripcion='zapatilla').save()
        MarcaModel(marcaNombre='nike2',
                    marcaDescripcion='zapatilla').save()
        MarcaModel(marcaNombre='nike3',
                    marcaDescripcion='zapatilla').save()
        MarcaModel(marcaNombre='nike4',
                    marcaDescripcion='zapatilla').save()
    

    def test_post_fail(self):
        '''Deberia fallar este test cuando no le pasamos informacion'''

        request = self.client.post('/manejoEc/marcas')
        message = request.data.get('message')
        
        self.assertEqual(request.status_code,400)
        self.assertEqual(message,'Error al crear la Marca')

    #Deberia funcionar este test
    def test_post_success(self):
        '''Deberia retornar la marca creaao'''

        request = self.client.post('/manejoEc/marcas', data={ 
        "marcaNombre":"Nike",
        "marcaDescripcion": "Nike para zapatos"
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('marcaId')
        
        marcaEncontrado = MarcaModel.objects.filter(marcaId=id).first()

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message,'Marca creado exitosamente')
        self.assertIsNotNone(marcaEncontrado)
    
    def test_get_success(self):
        '''Deberia retornar las marcas'''

        request = self.client.get(
            '/manejoEc/marcas', data={'pagina': 1, 'cantidad': 2})
        paginacion = request.data.get('paginacion')
        content = request.data.get('data').get('content')

        self.assertIsNone(paginacion.get('paginaPrevia'))
        self.assertIsNotNone(paginacion.get('paginaContinua'))
        self.assertEqual(paginacion.get('porPagina'), 2)
        self.assertEqual(len(content), 2)

    def test_put_succes(self):
        '''Deberia funcionar el actualizar'''

        objMarca :MarcaModel = MarcaModel.objects.all().first()
        id = objMarca.__getattribute__('marcaId')
        request = self.client.put(
            '/manejoEc/marca/'+str(id), data={ 
        "marcaNombre":"Nike2",
        "marcaDescripcion": "Nike para zapatos2"
        }, format='json')
        message = request.data.get('message')

        self.assertEqual(request.status_code,200)
        self.assertEqual(message,'Marca actualizada exitosamente')
    
    def test_put_fail(self):
        '''Deberia de fallar el actualizar'''

        request = self.client.put('/manejoEc/marca/90')
        message = request.data.get('message')

        self.assertEqual(request.status_code,404)
        self.assertEqual(message,'Marca no encontrada')

class ProductoTestCase(APITestCase):

    def setUp(self):
        MarcaModel(marcaNombre='nike',
                    marcaDescripcion='zapatilla').save()
        # ProductoModel(productoNombre='Nike',
        #                 productoPrecio=20.76,
        #                 productoFoto='/url',
        #                 productoCantidad=7,
        #                 productoTalla=['1','20','48'],
        #                 marca=22).save()

    def test_get_success(self):
        '''Deberia retornar el producto creado'''

        objMarca :MarcaModel = MarcaModel.objects.all().first()
        # objProducto = ProductoModel.objects.all().first()
        # print(objProducto)        
        id = objMarca.__getattribute__('marcaId')
        # print(id)
        # print(id)
        # print(id)
        request = self.client.post('/manejoEc/productos', data={ 
        "productoNombre": "Nike x2",
        "productoPrecio": 89.90,
        "productoCantidad": 12,
        "productoTalla":'1,  2,  3,4  ',
        "marca":int(id)
        }, format='multipart')
        message = request.data.get('message')
        # id = request.data.get('content').get('productoId')
        
        # productoEncontrado = ProductoModel.objects.filter(productoId=id).first()
        # marca: MarcaModel = MarcaModel.objects.all().first()
        
        # print(marca)
        # print(productoEncontrado)
        # print(request.status_code)

        # self.assertEqual(request.status_code, 201)
        self.assertEqual(message,'Producto creado exitosamente')
        # self.assertIsNotNone(marcaEncontrado)                

    



    


