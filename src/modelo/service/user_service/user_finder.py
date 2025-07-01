"""
    Busqueda de los usuarios por alias
"""

from src.modelo.entities.usuario import Usuario
from src.modelo.database_management.base.declarative_base import session

class UserFinder:
    @staticmethod
    def recover_by_alias(alias: str):
        return session.query(Usuario.Alias).filter(Usuario.Alias.ilike(f"%{alias}%")).limit(5).all()
