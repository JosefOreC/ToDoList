"""
    Archivo que almacena la clase encargada de la recuperación de datos filtrados
"""
from src.modelo.database_management.base.declarative_base import session
from src.modelo.entities.tarea import Tarea
from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.service.data_service.data_format import DataFormat
from sqlalchemy import or_
from datetime import date

class TaskFinder:
    """
        Clase encargada de la recuperacion de datos de la tarea con filtro de datos (buscador)
    """
    @staticmethod
    def search_for_tasks_by_name(id_usuario: int, nombre: str, archivado:bool=False):
        """
        filtro por nombre
        :param id_usuario: entero int
        :param nombre: un string del nombre str
        :param archivado: archivado o no bool
        :return: tupla de datos con los datos necesarios
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        Tarea.Nombre.ilike(f"%{nombre}%"), Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())

    @staticmethod
    def search_for_task_by_date(id_usuario: int, fecha_ini: date or str= None, fecha_fin: date or str = None,
                                archivado:bool=False):
        """
        filtro por fecha
        :param id_usuario: entero
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de las tareas necesarias
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        *fechas, Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())

    @staticmethod
    def search_for_task_by_date_and_name(id_usuario: int, nombre:str, fecha_ini: date or str=None,
                                         fecha_fin: date or str=None, archivado:bool=False):
        """
        filtro por fecha y nombre
        :param id_usuario: entero
        :param nombre: str de nombre a buscar
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de lo necesario para la tarea
        """

        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, Tarea.Nombre.ilike(f'%{nombre}%'),
                        *fechas, Tarea.Activo==True,
                        UsuarioTarea.Archivado == archivado).all())

    @staticmethod
    def search_for_task_by_check(id_usuario: int, realizado: bool, archivado: bool = False):

        """
        filtro por realizado
        :param id_usuario:
        :param realizado:
        :param archivado:
        :return:
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado==realizado,
                        UsuarioTarea.Archivado == archivado, Tarea.Activo==True).all())

    @staticmethod
    def search_for_task_by_check_name(id_usuario: int, nombre: str, realizado: bool, archivado: bool = False):
        """
        filtro por realizado
        :param id_usuario:
        :param nombre: str
        :param realizado:
        :param archivado:
        :return:
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, Tarea.Nombre.ilike(f'%{nombre}%')).all())

    @staticmethod
    def search_for_task_by_check_date(id_usuario: int, realizado: bool, fecha_ini: date or str=None,
                                      fecha_fin: date or str =None,archivado: bool = False):
        """
        filtro por realizado y fechas
        :param id_usuario:
        :param realizado:
        :param fecha_ini:
        :param fecha_fin:
        :param archivado:
        :return:
        retorna una tupla de los datos necesarios de una tarea
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, *fechas, Tarea.Activo==True).all())


    @staticmethod
    def search_for_task_by_check_date_name(id_usuario: int, nombre:str, realizado: bool, fecha_ini: date or str=None,
                                           fecha_fin: date or str=None,archivado: bool = False):
        """

        :param id_usuario:
        :param nombre:
        :param realizado:
        :param fecha_ini:
        :param fecha_fin:
        :param archivado:
        :return:
        retorna una tupla de los datos necesarios de una tarea
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, *fechas, Tarea.Nombre.ilike(f'%{nombre}%')
                        , Tarea.Activo==True).all())


    @staticmethod
    def search_for_tasks_by_group(id_usuario: int, id_grupo: int, archivado = False):
        """
        filtro por grupo
        :param id_usuario: entero int
        :param archivado: archivado o no bool
        :param id_grupo: int
        :return: tupla de datos con los datos necesarios
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        UsuarioTarea.IDGrupo == id_grupo, Tarea.Activo == True,
                        UsuarioTarea.Archivado == archivado, UsuarioTarea.IDGrupo == id_grupo).all())

    @staticmethod
    def search_for_tasks_by_name_group(id_usuario: int, id_grupo: int, nombre: str, archivado: bool = False):
        """
        filtro por nombre
        :param id_usuario: entero int
        :param nombre: un string del nombre str
        :param archivado: archivado o no bool
        :param id_grupo: int
        :return: tupla de datos con los datos necesarios
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        Tarea.Nombre.ilike(f"%{nombre}%"), Tarea.Activo == True,
                        UsuarioTarea.Archivado == archivado, UsuarioTarea.IDGrupo == id_grupo).all())

    @staticmethod
    def search_for_task_by_date_group(id_usuario: int, id_grupo: int, fecha_ini: date or str = None,
                                      fecha_fin: date or str = None, archivado: bool = False):
        """
        filtro por fecha
        :param id_usuario: entero
        :param id_grupo: int
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de las tareas necesarias
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario,
                        *fechas, Tarea.Activo == True,
                        UsuarioTarea.Archivado == archivado, UsuarioTarea.IDGrupo == id_grupo).all())

    @staticmethod
    def search_for_task_by_date_and_name_group(id_usuario: int, id_grupo: int, nombre: str, fecha_ini: date or str=None,
                                               fecha_fin: date or str=None, archivado: bool = False):
        """
        filtro por fecha y nombre
        :param id_usuario: entero
        :param id_grupo: int
        :param nombre: str de nombre a buscar
        :param fecha_ini: date o str
        :param fecha_fin: date o str
        :param archivado: bool
        :return: tupla de datos de lo necesario para la tarea
        """

        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)
                .join(UsuarioTarea,UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, Tarea.Nombre.ilike(f'%{nombre}%'),
                        *fechas, Tarea.Activo == True,
                        UsuarioTarea.Archivado == archivado, UsuarioTarea.IDGrupo==id_grupo).all())

    @staticmethod
    def search_for_task_by_check_group(id_usuario: int, id_grupo: int, realizado: bool, archivado: bool = False):
        """
        filtro por realizado
        :param id_usuario:
        :param id_grupo: int
        :param realizado:
        :param archivado:
        :return:
        """
        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, UsuarioTarea.IDGrupo==id_grupo, Tarea.Activo==True).all())

    @staticmethod
    def search_for_task_by_check_date_group(id_usuario: int, id_grupo: int, realizado: bool, fecha_ini: date or str=None,
                                            fecha_fin: date or str=None, archivado: bool = False):
        """
        filtro por realizado y fechas
        :param id_usuario:
        :param id_grupo: int
        :param realizado:
        :param fecha_ini:
        :param fecha_fin:
        :param archivado:
        :return:
        retorna una tupla de los datos necesarios de una tarea
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, *fechas, UsuarioTarea.IDGrupo==id_grupo,
                        Tarea.Activo==True).all())

    @staticmethod
    def search_for_task_by_check_date_name_group(id_usuario: int, id_grupo: int, nombre: str, realizado: bool,
                                                 fecha_ini: date or str=None, fecha_fin: date or str=None
                                                 , archivado: bool = False):
        """
        filtro por grupo, realizado, fechas y nombre
        :param id_usuario:
        :param id_grupo: int
        :param nombre:
        :param realizado:
        :param fecha_ini:
        :param fecha_fin:
        :param archivado:
        :return:
        retorna una tupla de los datos necesarios de una tarea
        """
        if not fecha_ini and not fecha_fin:
            raise Exception("No existen los datos necesarios para la busqueda.")

        fechas = []
        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            fechas.append(Tarea.Fecha_programada >= fecha_ini)
        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            fechas.append(Tarea.Fecha_programada <= fecha_fin)

        fechas = tuple(fechas)

        return (session.query(Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado).join(UsuarioTarea,
                                                                                 UsuarioTarea.IDTarea == Tarea.IDTarea)
                .filter(UsuarioTarea.IDUsuario == id_usuario, UsuarioTarea.Realizado == realizado,
                        UsuarioTarea.Archivado == archivado, *fechas,
                         Tarea.Nombre.ilike(f'%{nombre}%'),
                        UsuarioTarea.IDGrupo==id_grupo, Tarea.Activo==True).all())

    @staticmethod
    def search_for_task_by(id_usuario, id_grupo: int=None, nombre: str=None, realizado: bool=None,
                                                 fecha_ini: date or str=None, fecha_fin: date or str=None
                                                 , archivado: bool = False, prioridad: list[int] = None):
        recuperacion = (Tarea, UsuarioTarea.Disponible, UsuarioTarea.Realizado,
                              UsuarioTarea.IDGrupo, UsuarioTarea.Archivado)

        argumentos = [UsuarioTarea.IDUsuario==id_usuario]

        if id_grupo:
            argumentos.append(UsuarioTarea.IDGrupo==id_grupo)

        if nombre:
            argumentos.append(Tarea.Nombre.ilike(f'%{nombre}%'))

        if realizado is not None:
            argumentos.append(UsuarioTarea.Realizado == realizado)

        if fecha_ini:
            fecha_ini = DataFormat.convertir_data_to_date(fecha_ini)
            argumentos.append(Tarea.Fecha_programada>=fecha_ini)

        if fecha_fin:
            fecha_fin = DataFormat.convertir_data_to_date(fecha_fin)
            argumentos.append(Tarea.Fecha_programada<=fecha_fin)

        if archivado is not None:
            argumentos.append(UsuarioTarea.Archivado == archivado)

        if prioridad:
            ors = []
            for pr in prioridad:
                ors.append(Tarea.Prioridad == pr)
            argumentos.append(or_(*tuple(ors)))

        argumentos = tuple(argumentos)

        return (session.query(*recuperacion).join(UsuarioTarea, UsuarioTarea.IDTarea==Tarea.IDTarea)
                .filter(*argumentos).all())




