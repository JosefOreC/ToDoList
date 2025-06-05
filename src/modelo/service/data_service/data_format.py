from src.modelo.entities.tarea import Tarea
from datetime import datetime, date
from src.modelo.service.group_service.group_service_data import GroupServiceData as gsd
from src.modelo.service.session_service.session_manager import SessionManager


class DataFormat:
    @staticmethod
    def convertir_fecha(fecha: str):
        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha, "%d-%m-%Y").date()
            except:
                raise ValueError("Formato de fecha no soportado")
        elif isinstance(fecha, datetime):
            return fecha.date()
        elif isinstance(fecha, date):
            return fecha
        else:
            raise ValueError("Formato de fecha no soportado")

    @staticmethod
    def convert_to_dict_task_data(tareas: [Tarea, bool, bool, int]):
        response = []

        for tarea, dis, rea, id_grupo in tareas:
            if not tarea.Activo:
                continue
            grupo = gsd.get_data_task_group_name(id_grupo)
            rol = gsd.get_rol_in_group(SessionManager.get_id_user(), id_grupo)
            summary = {'id_tarea': tarea.IDTarea,
                       'nombre': tarea.Nombre,
                       'disponible': dis,
                       'realizado': rea,
                       'fecha': tarea.Fecha_programada.strftime("%d-%m-%Y"),
                       'prioridad': tarea.Prioridad,
                       'activo': tarea.Activo,
                       'detalle': tarea.Detalle,
                       'grupo': grupo,
                       'rol': rol,
                       'id_grupo': id_grupo,
                       'is_in_group': True if id_grupo else False
                       }
            response.append(summary)

        return response
