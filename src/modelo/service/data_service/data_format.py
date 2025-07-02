"""
data_format.py

Este módulo proporciona funciones utilitarias para formatear y convertir
datos relacionados con tareas, como fechas y estructuras de salida compatibles
con interfaces de usuario o APIs. Incluye integración con servicios de grupos
y manejo de sesiones.
"""


from src.modelo.entities.tarea import Tarea
from src.modelo.entities.grupo import Grupo
from datetime import datetime, date

from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.service.group_service.group_service_data import GroupServiceData
from src.modelo.service.session_service.session_manager import SessionManager
from src.modelo.entities.rol import Rol

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
    def convert_to_dict_groups_data(grupos: list):
        """

        :param grupos:
        :return:
        """
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
    def convert_to_dict_groups_data_with_out_rol(grupos: list):
        lista_grupo = []
        for grupo in grupos:
            lista_grupo.append(DataFormat.convert_to_dict_group_data(grupo))
        return lista_grupo

    @staticmethod
    def convert_to_dict_group_data(grupo: Grupo) -> dict:
        """

        :param grupo:
        :return:
        """
        return {
            'id_grupo': grupo.IDGrupo,
            'nombre': grupo.Nombre,
            'descripcion': grupo.Descripcion
        }

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

        for tarea, dis, rea, id_grupo, arc in tareas:
            if not tarea.Activo:
                continue
            if id_grupo:
                grupo = GroupServiceData.get_data_task_group_name(id_grupo)
                try:
                    rol = GroupServiceData.get_rol_in_group(SessionManager.get_id_user(), id_grupo).name
                except:
                    rol = None
            else:
                grupo = None
                rol = None
            summary = {'id_tarea': tarea.IDTarea,
                       'nombre': tarea.Nombre,
                       'disponible': dis,
                       'realizado': rea,
                       'archivado': arc,
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

    @staticmethod
    def convert_to_dict_tarea_to_edit(tarea: list[Tarea, UsuarioTarea] or tuple):
        task: Tarea
        user_manag: UsuarioTarea
        task, user_manag = tarea
        miembro: UsuarioTarea
        return {
            'tarea':{
                'id_tarea': task.IDTarea,
                'nombre': task.Nombre,
                'detalle': task.Detalle,
                'fecha': task.Fecha_programada,
                'prioridad': DataFormat.prioridades.get(task.Prioridad),
                'type_check': task.type_check #False: Individual, True: Grupal
            },
            'user':{
                'rol': user_manag.grupo.Nombre if user_manag.IDGrupo else Rol.master.name,
                'check': user_manag.Realizado,
                'archivado': user_manag.Archivado,
                'disponible': user_manag.Disponible, #Checkable o editable
            },
            'grupo': {
                'id_grupo': user_manag.IDGrupo,
                'nombre': user_manag.grupo.Nombre
            } if user_manag.IDGrupo else None
            ,
            'miembros':
                [{'alias': miembro.usuario.Alias,
                  'editable': miembro.Disponible,
                  'rol': GroupServiceData.get_rol_in_group(id_grupo= miembro.IDGrupo, id_usuario=miembro.IDUsuario).name
                        if GroupServiceData.is_user_in_group(id_grupo= miembro.IDGrupo, id_usuario=miembro.IDUsuario)
                        else 'Fuera del grupo',
                  'check': miembro.Realizado
                  } for miembro in task.tarea_usuarios] if user_manag.IDGrupo else None


        }

    @staticmethod
    def convert_to_dict_task_data_groups(tareas: list[Tarea, Rol]):
        """

        :param tareas:
        :return:
        """
        response = []

        for tarea, archivado, realizado, disponible in tareas:
            data = {'id_tarea': tarea.IDTarea,
                 'nombre': tarea.Nombre,
                 'disponible': disponible,
                 'realizado': realizado,
                 'fecha': tarea.Fecha_programada.strftime("%d-%m-%Y"),
                 'prioridad': DataFormat.prioridades.get(tarea.Prioridad),
                 'nombre_prioridad': DataFormat.prioridades.get(tarea.Prioridad),
                 'detalle': tarea.Detalle,
                 'archivado': archivado
            }
            response.append(data)

        return response

    @staticmethod
    def convert_to_dict_basic_data_user(usuario_data: tuple):
        """

        :param usuario_data:
        :return:
        """
        return {
            'alias': usuario_data[0],
            'pregunta': usuario_data[1],
            'respuesta':usuario_data[2]
        }

    @staticmethod
    def convert_to_dict_member_data_group(miembros: tuple or list)-> list[dict['alias', 'rol']]:
        """

        :param miembros:
        :return:
        """
        response = []
        for alias, rol in miembros:
            data = {
                'alias': alias,
                'rol': rol
            }
            response.append(data)

        return response