from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField
from .authManager import ManejoUsuarios
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, AbstractUser


# Create your models here.


class UsuarioModel(AbstractBaseUser,PermissionsMixin):
    
    TIPO_USUARIO = [(1,'ADMINISTRADOR'),(2,'OPERARIO'),(3,'CLIENTE')]

    usuarioId = models.AutoField(
        primary_key=True, null=False, db_column='id', unique=True)
    
    usuarioDni = models.CharField(max_length=8, db_column='dni')

    usuarioNombre = models.CharField(max_length=50, db_column='nombre')

    usuarioApellido = models.CharField(max_length=50, db_column='apellido', verbose_name='Apellido del usuario')

    usuarioCorreo = models.EmailField(
        max_length=50, db_column='email', unique=True)

    usuarioTipo = models.IntegerField(choices=TIPO_USUARIO, db_column='tipo')
    password = models.TextField(null=True)

    # configurar los campos base de nuestro modelo auth
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Todo lo siguiente es cuando vayamos a ingresar un administrador por consola

    objects = ManejoUsuarios()

    # definimos la columna que sera la encargada de validar  que el usuario sea unico e irrepetible
    USERNAME_FIELD = 'usuarioCorreo'

    REQUIRED_FIELDS = ['usuarioNombre','usuarioApellido','usuarioTipo','usuarioDni']

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

class PedidoModel(models.Model):
    pedidoId = models.AutoField(primary_key=True, db_column='id', unique=True)

    pedidoFecha = models.DateTimeField(auto_now_add=True, db_column='fecha')

    pedidoTotal = models.DecimalField(
        max_digits=5, decimal_places=2, db_column='total')

    cliente = models.ForeignKey(
        to=UsuarioModel, related_name='clientePedidos', db_column='cliente_id', on_delete=models.PROTECT)
    class Meta:
        db_table = 'pedidos'
class DetallePedidoModel(models.Model):
    detalleId = models.AutoField(primary_key=True, db_column='id', unique=True)

    detalleCantidad = models.IntegerField(
        db_column='cantidad', null=False, validators=[MinValueValidator(0, 'Valor no puede ser negativo')])

    detalleSubTotal = models.DecimalField(
        max_digits=7, decimal_places=2, db_column='sub_total')

    producto = models.ForeignKey(
        to=ProductoModel, related_name='productoDetalles', db_column='producto_id', on_delete=models.PROTECT)

    pedido = models.ForeignKey(
        to=PedidoModel, related_name='pedidoDetalles', db_column='pedido_id', on_delete=models.PROTECT)

    class Meta:
        db_table = 'detalles'