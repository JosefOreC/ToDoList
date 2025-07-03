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




