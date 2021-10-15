from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class  UsuarioModel(models.Model):
    TIPO_USUARIO = [(1, 'ADMINISTRADOR'), (2,'MANTENEDOR'), (3,'CLIENTE')]

    usuarioId = models.AutoField(
        primary_key=True, null=False, db_column='id', unique=True)
    
    usuarioDni = models.CharField(max_length=8, db_column='dni')

    usuarioNombre = models.CharField(max_length=50, db_column='nombre')

    usuarioApellido = models.CharField(max_length=50, db_column='apellido', verbose_name='Apellido del usuario')

    usuarioCorreo = models.EmailField(
        max_length=50, db_column='email', unique=True)

    usuarioTipo = models.IntegerField(choices=TIPO_USUARIO, db_column='tipo')

    password = models.TextField(null=True)

    class Meta:
        db_table = 'usuarios'
    

# class PedidoModel(models.Model):
#     pedidoId = models.AutoField(
#         primary_key=True, null=False,db_column='id',unique=True)
    
#     pedidoFecha = models.DateField(db_column='fecha',null=False)

#     pedidoTotal = models.DecimalField(max_digits=5,decimal_places=2, db_column='total')

#     cliente = models.ForeignKey(
#         to=UsuarioModel,related_name='clientePedidos', db_column='clienteId', on_delete=models.PROTECT)


class MarcaModel(models.Model):
    marcaId = models.AutoField(
        primary_key=True, null=False,db_column='id',unique=True)
    
    marcaNombre = models.CharField(max_length=100,db_column='nombre',null=False)

    marcaDescripcion = models.TextField(null=True)

    class Meta:
        db_table = 'marcas'
class ProductoModel(models.Model):
    productoId = models.AutoField(
        primary_key=True, null=False,db_column='id',unique=True)
    
    productoNombre = models.CharField(max_length=100, db_column='nombre',null=False)

    productoPrecio = models.DecimalField(
        db_column='precio', max_digits=5, decimal_places=2, null=False)
    
    productoFoto = models.CharField(max_length=130
        , db_column='foto', null=True)

    productoCantidad = models.IntegerField( db_column='cantidad', null=False, validators=[MinValueValidator(0, 'Valor no puede ser negativo')])

    productoTalla = ArrayField(ArrayField(models.CharField(max_length=2),db_column='talla',),)

    productoActualizado = models.DateTimeField(auto_now_add=True,db_column='updated_at')

    productoCreado = models.DateTimeField(db_column='created_at', auto_now_add=True)

    marca = models.ForeignKey(
        to=MarcaModel,related_name='marcaProducto', db_column='marca_id', on_delete=models.PROTECT)

    class Meta:
        db_table = 'productos'