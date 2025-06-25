"""
Clase que controla los datos de la entidad usuario
se basa en el control de querys: recuperación, actualización, inserción, eliminación de datos
"""

from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import Usuario, UsuarioGrupo, Grupo
from src.modelo.service.user_service.update_user import UpdateUser
from sqlalchemy.exc import IntegrityError

class UserServiceData:
    """
    Proporciona servicios relacionados al manejo de datos de usuarios en la base de datos.
    """

    @staticmethod
    def recover_user_for_alias(alias: str):
        """
        Recupera un usuario activo a partir de su alias.

        Args:
            alias (str): Alias del usuario.

        Returns:
            Usuario: Instancia del usuario si existe y está activo, de lo contrario None.
        """
        return session.query(Usuario).filter_by(Alias=alias, Estado=True).first()

    @staticmethod
    def get_user_for_id_user(id_usuario):
        """
        Recupera un usuario activo a partir de su ID.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            Usuario: Instancia del usuario si existe y está activo, de lo contrario None.
        """
        return session.query(Usuario).filter_by(IDUsuario=id_usuario, Estado=True).first()

    @staticmethod
    def recover_id_user_for_alias(alias: str):
        """
        Recupera el ID de un usuario activo a partir de su alias.

        Args:
            alias (str): Alias del usuario.

        Returns:
            int: ID del usuario.

       Raises:
           IndexError: Si no se encuentra un usuario con el alias dado.
       """
        return session.query(Usuario.IDUsuario).filter_by(Alias=alias, Estado=True).first()[0]

    @staticmethod
    def is_user_with_alias_exits(alias: str):
        return True if session.query(1).filter(Usuario.Alias==alias, Usuario.Estado==True).first() else False

    @staticmethod
    def insert_new_user(usuario: Usuario):
        try:
            session.add_all([usuario])
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception("El alias ya está ocupado.")

    @staticmethod
    def __get_all_users():
        return session.query(Usuario.Alias, Usuario.Nombres, Usuario.Apellidos, Usuario.Estado).all()
    @staticmethod
    def update_user(usuario: int or str or Usuario, nombres=None, apellidos=None, alias = None, password= None):

        update_data = UpdateUser(usuario)
        if nombres:
            update_data.update_nombres(nombres)
        if apellidos:
            update_data.update_apellidos(apellidos)
        try:
            if alias:
                update_data.update_alias(alias)
            if password:
                update_data.update_password(password)

            session.commit()

        except IntegrityError:
            session.rollback()
            raise Exception("El alias ya está ocupado.")

        except Exception as E:
            session.rollback()
            raise Exception(E)

    @staticmethod
    def recover_basic_data_user(alias: str):
        """
        :param alias:
        :return:
        tupla con los datos basicos de los clientes (alias, pregunta, respuesta)
        """

        if not UserServiceData.is_user_with_alias_exits(alias):
            raise Exception(f"El usuario '{alias}' no existe.")

        return session.query(Usuario.Alias, Usuario.Pregunta, Usuario.Respuesta).filter_by(Alias=alias).first()

    @staticmethod
    def soft_delete_user(id_usuario):
        usuario = UserServiceData.get_user_for_id_user(id_usuario)
        usuario.Estado = False
        session.commit()
