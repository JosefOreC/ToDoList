"""
    Clase que controla los datos de un usuario para ser actualizado
    no se relaciona directamente con la base de datos.
"""

from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import Usuario, UsuarioGrupo
import bcrypt




class UpdateUser:

    __usuario = Usuario
    def __init__(self, usuario: int or Usuario):
        self.__recover_usuario(usuario)

    def __recover_usuario(self, usuario):
        if isinstance(usuario, int):
            self.__usuario = session.query(Usuario).filter_by(IDUsuario = usuario).first()
            return
        self.__usuario = usuario

    @staticmethod
    def update_rol(id_usuario, id_grupo, rol):
        usuario_grupo : UsuarioGrupo
        usuario_grupo = session.query(UsuarioGrupo).filter_by(IDGrupo=id_grupo,
                                                              IDUsuario=id_usuario)
        usuario_grupo.rol = rol

    def update_estado(self, estado):
        self.__usuario.Estado = estado

    def update_nombres(self, nombres):
        self.__usuario.Nombres = nombres

    def update_apellidos(self, apellidos):
        self.__usuario.Apellidos = apellidos

    def update_alias(self, alias):
        self.__usuario.Alias = alias

    def update_password(self, password):
        new_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.__usuario.Password = new_password