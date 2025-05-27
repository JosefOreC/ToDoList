"""
    Crea los metodos intermedios para el uso de Usuario
"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.usuario import Usuario

class UserService:
    @staticmethod
    def recover_user_for_alias(alias: str):
        return session.query(Usuario).where(Alias = alias).first()

