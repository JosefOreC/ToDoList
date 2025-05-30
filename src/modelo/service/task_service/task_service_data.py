"""


"""

from src.modelo.entities.base.declarative_base import session
from src.modelo.entities.usuario import Usuario
from src.modelo.entities.usuario_grupo import UsuarioGrupo
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.grupo import Grupo
from src.modelo.entities.tarea import Tarea
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.format_data import DataFormat, datetime
from datetime import date, timedelta

class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: UsuarioTarea):
        session.add_all([tarea])
        session.flush()
        usuario_tarea.IDTarea = tarea.IDTarea
        session.add_all([usuario_tarea])
        session.commit()

    @staticmethod
    def get_tasks_user_list_date(usuario_id: int, fecha_inicio: str or date, fecha_fin: str or date = None):
        fecha_inicio = DataFormat.convertir_fecha(fecha_inicio)
        if not fecha_fin:
            fecha_fin = fecha_inicio
        else:
            fecha_fin = DataFormat.convertir_fecha(fecha_fin)

        if fecha_fin < fecha_inicio:
            raise Exception(f'La fecha de inicio {fecha_inicio} es mayor a la fecha de fin {fecha_fin}. '
                            f'\nNo se recuperó datos.')
        resultados = session.query(Tarea,
                                   UsuarioTarea.Disponible,
                                   UsuarioTarea.Realizado).join(UsuarioTarea,
                                   UsuarioTarea.IDUsuario==usuario_id).filter(UsuarioTarea.IDTarea==Tarea.IDTarea,
                                   Tarea.Fecha_programada >= fecha_inicio,
                                   Tarea.Fecha_programada <= fecha_fin).order_by(Tarea.Prioridad.asc()).all()
        return resultados

    @staticmethod
    def get_tasks_session_user_list_date(fecha: str or date):
        usuario_id = SessionManager.get_instance().usuario.IDUsuario
        return TaskServiceData.get_tasks_user_list_date(usuario_id, fecha)

    @staticmethod
    def get_tasks_session_user_list_today():
        fecha = date.today()
        return TaskServiceData.get_tasks_session_user_list_date(fecha)
