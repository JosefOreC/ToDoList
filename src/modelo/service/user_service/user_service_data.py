"""
    Clase que controla los datos de la entidad usuario
    se basa en el control de querys: recuperación, actualización, inserción, eliminación de datos
"""

from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import Usuario, UsuarioGrupo, Grupo
from src.modelo.service.user_service.update_user import UpdateUser
from sqlalchemy.exc import IntegrityError

class UserServiceData:
    @staticmethod
    def recover_user_for_alias(alias: str):
        return session.query(Usuario).filter_by(Alias=alias).first()

    @staticmethod
    def recover_id_user_for_alias(alias: str):
        return session.query(Usuario.IDUsuario).filter_by(Alias=alias).first()[0]

    @staticmethod
    def is_user_with_alias_exits(alias: str):
        return True if session.query(1).filter(Usuario.Alias==alias).first() else False

    @staticmethod
    def insert_new_user(usuario: Usuario):
        try:
            session.add_all([usuario])
            session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception("El alias ya está ocupado.")

    @staticmethod
    def update_user(usuario: str or Usuario, nombres=None, apellidos=None, alias = None, estado = None, password= None):

        update_data = UpdateUser(usuario)
        if nombres:
            update_data.update_nombres(nombres)
        if apellidos:
            update_data.update_apellidos(apellidos)
        try:
            if alias:
                update_data.update_alias(alias)
            if estado is not None:
                update_data.update_estado(estado)
            if password:
                update_data.update_password(password)

            session.commit()

        except IntegrityError:
            session.rollback()
            raise Exception("El alias ya está ocupado.")

        except Exception as E:
            session.rollback()
            raise Exception(E)

