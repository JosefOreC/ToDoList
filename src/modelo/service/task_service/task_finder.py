"""
    Archivo que almacena la clase encargada de la recuperación de datos filtrados
"""
from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.tarea import Tarea
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.service.data_service.data_format import DataFormat
from datetime import date

class TaskFinder:
    """
        Clase encargada de la recuperacion de datos de la tarea con filtro de datos (buscador)
    """
    @staticmethod
    def search_for_tasks_by_name(id_usuario: int, filtro: str, archivado:bool=False):
        """
        :param id_usuario: entero int
        :param filtro: un string del nombre str
        :param archivado: archivado o no bool
        :return: tupla de datos con los datos necesarios
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDUsuario==id_usuario)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        Tarea.Nombre.ilike(f"%{filtro}%"), Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())

    @staticmethod
    def search_for_task_by_date(id_usuario: int, fecha_ini: date or str, fecha_fin: date or str = None,
                                archivado:bool=False):
        """
        :param id_usuario: entero
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de las tareas necesarias
        """
        fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
        fecha_fin = DataFormat.convertir_data_to_date(fecha_fin) if fecha_fin else fecha_ini

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDUsuario==id_usuario)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        Tarea.Fecha_programada>=fecha_ini, Tarea.Fecha_programada<=fecha_fin, Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())

    @staticmethod
    def search_for_task_by_date_and_name(id_usuario: int, nombre:str, fecha_ini: date or str, fecha_fin: date or str,
                                         archivado:bool=False):
        """

        :param id_usuario: entero
        :param nombre: str de nombre a buscar
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de lo necesario para la tarea
        """

        fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
        fecha_fin = DataFormat.convertir_data_to_date(fecha_fin) if fecha_fin else fecha_ini

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDUsuario==id_usuario)
                .filter(UsuarioTarea.IDUsuario == id_usuario, Tarea.Nombre.ilike(f'%{nombre}%'),
                        Tarea.Fecha_programada>=fecha_ini, Tarea.Fecha_programada<=fecha_fin, Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())





