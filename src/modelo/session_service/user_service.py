"""
    Crea los metodos intermedios para el uso de Usuario
"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.usuario import Usuario
from src.modelo.entities.usuario_grupo import UsuarioGrupo
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.tarea import Tarea

class UserService:
    @staticmethod
    def recover_user_for_alias(alias: str):
        return session.query(Usuario).where(Usuario.Alias == alias).first()

