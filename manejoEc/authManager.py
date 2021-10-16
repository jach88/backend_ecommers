from django.contrib.auth.models import BaseUserManager

class ManejoUsuarios(BaseUserManager):

    def create_user(self, email,nombre,apellido,tipo,dni,password=None):
        """Creacion de un usuario"""
        if not email:
            raise ValueError('El usuario tiene que tener un correo valido')
        #valida el correo y lo normaliza haciendolo en minusculas
        email = self.normalize_email(email)

        usuarioCreado = self.model(usuarioCorreo=email, usuarioNombre=nombre,
                                   usuarioApellido=apellido, usuarioTipo=tipo,usuarioDni=dni)

        usuarioCreado.set_password(password)
        usuarioCreado.save(using=self._db)

        return usuarioCreado
    
    def create_superuser(self, usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo,usuarioDni, password):
        '''Creacion de un super usuario (administrador)'''
        # los parametros que va a recibir tienen que ser los mismos que hubiesemos declarado en el usuarioModel REQUIRED_FIELD y en el USERNAME_FIELD , llegaran con esos mismo nombre de parametros y en el caso que se escribiese mal, lanzara un error de argumento inesperado

        nuevoUsuario = self.create_user(
            usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo,usuarioDni, password)

        nuevoUsuario.is_superuser = True
        nuevoUsuario.is_staff = True
        nuevoUsuario.save(using=self._db)