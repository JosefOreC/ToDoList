"""
    Crea los metodos intermedios para el uso de Usuario
"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.modelo import Usuario
from src.modelo.service.user_service.update_user import UpdateUser

class UserService:
    @staticmethod
    def recover_user_for_alias(alias: str):
        return session.query(Usuario).where(Usuario.Alias == alias).first()

    @staticmethod
    def is_user_with_alias_exits(alias: str):
        return True if session.query(1).where(Usuario.Alias == alias).all() else False

    @staticmethod
    def insert_new_user(usuario: Usuario):
        session.add_all([usuario])
        session.commit()

    @staticmethod
    def update_user(usuario: str or Usuario, nombres=None, apellidos=None, alias = None, estado = None, password = None):
        update_data = UpdateUser(usuario)
        if nombres:
            update_data.update_nombres(nombres)
        if apellidos:
            update_data.update_apellidos(apellidos)
        if alias:
            update_data.update_alias(alias)
        if estado != None:
            update_data.update_estado(estado)
        if password:
            update_data.update_password(password)

        update_data.do_changes()


