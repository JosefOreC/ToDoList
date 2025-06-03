"""
    Clase que controla la entidad tarea y relacionados
    desde la base de datos CRUD.
"""

from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.modelo import UsuarioTarea, Tarea, Grupo
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.service.data_service.data_format import DataFormat
from datetime import date
from src.modelo.service.task_service.update_task import UpdateTask

class TaskServiceData:
    @staticmethod
    def insert_task_user(tarea: Tarea, usuario_tarea: UsuarioTarea):
        session.add_all([tarea])
        session.flush()
        usuario_tarea.IDTarea = tarea.IDTarea
        session.add_all([usuario_tarea])
        session.commit()

    @staticmethod
    def update_task_user(id_usuario, id_tarea, nombre = None, activo = None,
                         fecha = None, prioridad = None, disponible = None,
                         realizado = None, detalle = None):

        updatedata = UpdateTask(id_tarea, id_usuario)

        if nombre:
            updatedata.update_name(nombre)
        if activo:
            updatedata.update_activo(activo)
        if fecha:
            updatedata.update_fecha(fecha)
        if prioridad:
            updatedata.update_prioridad(prioridad)
        if disponible != None:
            updatedata.update_disponible(disponible)
        if realizado != None:
            updatedata.update_realizado(realizado)
        if detalle:
            updatedata.update_detalle(detalle)

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
                                   UsuarioTarea.Realizado, UsuarioTarea.IDGrupo).join(UsuarioTarea,
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
        return TaskServiceData.get_tasks_session_user_list_date(date.today())





