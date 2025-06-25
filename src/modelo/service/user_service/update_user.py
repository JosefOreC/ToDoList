"""
Clase que controla los datos de un usuario para ser actualizado
no se relaciona directamente con la base de datos.
"""

from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import Usuario, UsuarioGrupo
import bcrypt


class UpdateUser:
    """
    Clase para actualizar los atributos de un usuario (Usuario) y su relación con grupos (UsuarioGrupo).
    """

    __usuario = Usuario
    def __init__(self, usuario: int or Usuario):
        """
        Inicializa la clase UpdateUser con una instancia de Usuario o un ID de usuario.

        Args:
            usuario (int or Usuario): Instancia del usuario o su ID.
        """
        self.__recover_usuario(usuario)

    def __recover_usuario(self, usuario):
        """
        Recupera la instancia del usuario desde la base de datos si se proporciona un ID.

        Args:
            usuario (int or Usuario): ID del usuario o instancia.
        """
        if isinstance(usuario, int):
            self.__usuario = session.query(Usuario).filter_by(IDUsuario = usuario).first()
            return
        if isinstance(usuario, str):
            self.__usuario = session.query(Usuario).filter_by(Alias = usuario).first()
            return
        self.__usuario = usuario

    @staticmethod
    def update_rol(id_usuario, id_grupo, rol):
        """
        Actualiza el rol de un usuario dentro de un grupo.

        Args:
            id_usuario (int): ID del usuario.
            id_grupo (int): ID del grupo.
            rol (Rol): Nuevo rol que se asignará al usuario.
        """
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
        """
        Actualiza el alias del usuario.

        Args:
            alias (str): Nuevo alias.
        """
        self.__usuario.Alias = alias

    def update_password(self, password):
        """
        Actualiza la contraseña del usuario, encriptándola con bcrypt.

        Args:
            password (str): Nueva contraseña en texto plano.
        """
        new_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.__usuario.Password = new_password

