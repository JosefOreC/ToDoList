from src.modelo.entities.tarea import Tarea
from datetime import datetime, date

class DataFormat:
    @staticmethod
    def convertir_fecha(fecha: str):
        if isinstance(fecha, str):
            return datetime.strptime(fecha, "%d-%m-%Y").date()
        elif isinstance(fecha, datetime):
            return fecha.date()
        elif isinstance(fecha, date):
            return fecha
        else:
            raise ValueError("Formato de fecha no soportado")

    @staticmethod
    def summarize_task_data_main_view(tareas: [Tarea, bool, bool]):
        response = []

        for tarea, dis, rea in tareas:
            if not tarea.Activo:
                continue
            summary = {'id': tarea.IDTarea,
                       'nombre': tarea.Nombre,
                       'disponible': dis,
                       'realizado': rea,
                       'fecha': tarea.Fecha_programada,
                       'prioridad': tarea.Prioridad,
                       'activo': tarea.Activo}
            response.append(summary)

        return response
