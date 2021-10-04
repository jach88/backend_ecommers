from django.db import models

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
    

class PedidoModel(models.Model):
    pedidoId = models.AutoField(
        primary_key=True, null=False,db_column='id',unique=True)
    
    pedidoFecha = models.DateField(db_column='fecha',null=False)

    pedidoTotal = models.DecimalField(max_digits=5,decimal_places=2, db_column='total')

    cliente = models.ForeignKey(
        to=UsuarioModel,related_name='clientePedidos', db_column='clienteId', on_delete=models.PROTECT)
    