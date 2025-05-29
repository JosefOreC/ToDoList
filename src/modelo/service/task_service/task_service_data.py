"""


"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.usuario import Usuario
from src.modelo.entities.usuario_grupo import UsuarioGrupo
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager
from sqlalchemy.orm import joinedload
from src.modelo.format_data import DataFormat, datetime

class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: UsuarioTarea):
        session.add_all([tarea])
        session.flush()
        usuario_tarea.IDTarea = tarea.IDTarea
        session.add_all([usuario_tarea])
        session.commit()

    @staticmethod
    def get_tasks_user_list_date(fecha: str or datetime):
        if type(fecha) == str:
            fecha = DataFormat.convertir_fecha(fecha)
        tareas_filtradas = (
            session.query(UsuarioTarea)
            .join(Usuario, UsuarioTarea.IDUsuario == Usuario.IDUsuario)
            .join(Tarea, UsuarioTarea.IDTarea == Tarea.IDTarea)
            .filter(
                Usuario.IDUsuario == SessionManager.get_instance().usuario.IDUsuario,
                Tarea.Fecha_programada == fecha
            )
            .all()
        )

        return tareas_filtradas


