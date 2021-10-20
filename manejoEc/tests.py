from django.test import TestCase
from rest_framework.test import APITestCase
from .models import MarcaModel

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
        '''Deberia retornar el producto creado'''

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
        id = objMarca._getattribute_('marcaId')
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