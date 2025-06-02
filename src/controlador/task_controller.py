from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.tarea import Tarea
from src.modelo.service.task_service.register_task import RegisterTask, TaskServiceData
from src.modelo.service.data_service.data_format import DataFormat

class TaskController:
    @staticmethod
    def recover_tasks_today():
        try:
            resultados = TaskServiceData.get_tasks_session_user_list_today()
        except Exception as E:
            return False, f"No se pudo recuperar las tareas. \n{E}"

        if not resultados:
            return True, None

        return True, resultados

    @staticmethod
    def event_register_task_user(nombre: str, fecha: str, prioridad: int, detalle: str):
        try:
            fecha = DataFormat.convertir_fecha(fecha)
        except Exception as E:
            return False, f"Fecha no valida. Error {E}"

        try:
            prioridad = int(prioridad)
            if prioridad <=0 or prioridad >= 5:
                return False, "Prioridad no válida, tiene que estar el 1 al 5."
        except ValueError as E:
            return False, E
        except TypeError as E:
            return False, E

        tarea = Tarea(Nombre=nombre, Fecha_programada=fecha, Prioridad=prioridad, Detalle = detalle)
        return RegisterTask(tarea).register_task()

    @staticmethod
    def event_update_task_user(id_usuario, id_tarea, nombre = None, activo = None,
                         fecha = None, prioridad= None, disponible=None,
                         realizado = None, detalle = None):
        if not(nombre or activo or fecha or prioridad or detalle) and disponible==None and realizado==None:
            return False, 'No hubo cambios.'

        try:
            TaskServiceData.update_task_user(id_usuario, id_tarea, nombre,
                                             activo, fecha, prioridad,
                                             disponible, realizado, detalle)
            return True, 'Se guardaron los cambiós con exito'
        except Exception as E:
            return False, f'No se guardaron los cambios. \n{E}'

    @staticmethod
    def event_update_task_session_manager(id_tarea, nombre=None, activo=None,
                               fecha=None, prioridad=None, disponible=None,
                               realizado=None):

        return TaskController.event_update_task_user(SessionManager.get_instance().usuario.IDUsuario,
                                                     id_tarea, nombre, activo,
                                                     fecha, prioridad, disponible,
                                                     realizado)