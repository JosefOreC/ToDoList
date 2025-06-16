"""
data_format.py

Este módulo proporciona funciones utilitarias para formatear y convertir
datos relacionados con tareas, como fechas y estructuras de salida compatibles
con interfaces de usuario o APIs. Incluye integración con servicios de grupos
y manejo de sesiones.
"""
from sqlalchemy.testing import fails_on_everything_except

from src.modelo.entities.tarea import Tarea
from datetime import datetime, date
from src.modelo.service.group_service.group_service_data import GroupServiceData as gsd
from src.modelo.service.session_service.session_manager import SessionManager


class DataFormat:
    """Clase utilitaria para formateo y conversión de datos relacionados con tareas."""

    prioridades = {1: 'Muy Alta', 2: 'Alta', 3: 'Media', 4: 'Baja', 5: 'Muy Baja'}

    @staticmethod
    def convertir_data_to_date(fecha: str):
        """Convierte una cadena o un objeto datetime o date a un objeto date.

        Soporta:
            - String con formato "dd-mm-aaaa"
            - Objeto datetime
            - Objeto date

        Args:
            fecha (str | datetime | date): Fecha en formato string o como objeto datetime o date.

        Returns:
            date: Objeto date convertido.

        Raises:
            ValueError: Si el formato de la fecha no es soportado o inválido.
                """
        if isinstance(fecha, date):
            return fecha

        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha, "%d-%m-%Y").date()
            except:
                raise ValueError("Formato de fecha no soportado")

        if isinstance(fecha, datetime):
            return fecha.date()

        raise ValueError("Formato de fecha no soportado")

    @staticmethod
    def convertir_date_to_str(fecha: datetime or date):
        if isinstance(fecha, datetime or date):
            return fecha.strftime("%d-%m-%Y")
        raise ValueError("Tipo de dato no soportado")

    @staticmethod
    def convert_to_dict_group_data(grupos: list):
        data = []

        for grupo in grupos:
            dato = {
                'id_grupo': grupo[0],
                'nombre': grupo[1],
                'descripcion': grupo[2],
                'rol_usuario': grupo[3].name
            }
            data.append(dato)

        return data

    @staticmethod
    def convert_to_dict_task_data(tareas: list[Tarea, bool, bool, int]):
        """Convierte una lista de tareas y su información asociada en una lista de diccionarios.

        Cada elemento de la lista de entrada debe tener la forma:
        (Tarea, disponible: bool, realizado: bool, id_grupo: int)

        Solo incluye tareas activas y agrega información del grupo y rol si el id_grupo existe.

        Args:
            tareas (list): Lista de tuplas con datos de tarea, disponibilidad, realización y grupo.

        Returns:
            list: Lista de diccionarios con los datos de las tareas formateados para salida o API.
        """
        response = []

        for tarea, dis, rea, id_grupo in tareas:
            if not tarea.Activo:
                continue
            if id_grupo:
                grupo = gsd.get_data_task_group_name(id_grupo)
                rol = gsd.get_rol_in_group(SessionManager.get_id_user(), id_grupo).name
            else:
                grupo = None
                rol = None
            summary = {'id_tarea': tarea.IDTarea,
                       'nombre': tarea.Nombre,
                       'disponible': dis,
                       'realizado': rea,
                       'fecha': tarea.Fecha_programada.strftime("%d-%m-%Y"),
                       'prioridad': tarea.Prioridad,
                       'nombre_prioridad': DataFormat.prioridades.get(tarea.Prioridad),
                       'activo': tarea.Activo,
                       'detalle': tarea.Detalle,
                       'grupo': grupo,
                       'rol': rol,
                       'id_grupo': id_grupo,
                       'is_in_group': True if id_grupo else False
                       }
            response.append(summary)

        return response
