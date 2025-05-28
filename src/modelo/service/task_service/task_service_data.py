"""


"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.usuario import Usuario
from src.modelo.entities.usuario_grupo import UsuarioGrupo
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager

class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: UsuarioTarea):
        session.add_all([tarea])
        session.flush()
        usuario_tarea.IDTarea = tarea.IDTarea
        session.add_all([usuario_tarea])
        session.commit()


