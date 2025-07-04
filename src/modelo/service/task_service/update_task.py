"""
Controla los datos de una tarea para su actualización
no se involucra con la base de datos.
"""
from sys import exception

from sqlalchemy import false

from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.tarea import Tarea
from src.modelo.database_management.base.declarative_base import session

class UpdateTask:
    """
    Clase encargada de realizar actualizaciones en los atributos de una tarea (Tarea)
    y su relación con un usuario (UsuarioTarea) sin aplicar commit a la base de datos.
    """

    def __init__(self, id_tarea, id_usuario=None):
        """
        Inicializa el actualizador de tarea y recupera las entidades correspondientes.

        Args:
            id_tarea (int): ID de la tarea a actualizar.
            id_usuario (int, optional): ID del usuario relacionado con la tarea.
        """
        self.id_tarea = id_tarea
        self.id_usuario = id_usuario
        self.__recover_tarea()


    def __recover_tarea(self):
        """
        Recupera las instancias de Tarea y UsuarioTarea asociadas.
        """
        self.__tarea = session.query(Tarea).filter_by(IDTarea=self.id_tarea).first()
        self.__usuario_tarea = session.query(UsuarioTarea).filter_by(IDTarea = self.id_tarea,
                                                               IDUsuario = self.id_usuario).first()

    def update_name(self, nombre):
        """
        Actualiza el nombre de la tarea.

        Args:
            nombre (str): Nuevo nombre para la tarea.
        """
        self.__tarea.Nombre = nombre

    def update_activo(self, activo):
        """
        Actualiza el estado activo/inactivo de la tarea.

        Args:
            activo (bool): True para activa, False para inactiva.
        """
        self.__tarea.Activo = activo

    def update_archivado(self, archivado):
        self.__usuario_tarea.Archivado = archivado

    def update_fecha(self, fecha):
        self.__tarea.Fecha_programada = fecha

    def update_prioridad(self, prioridad):
        self.__tarea.Prioridad = prioridad

    def update_disponible(self, disponible):
        self.__usuario_tarea.Disponible = disponible

    def update_realizado(self, realizado):
        """
        Actualiza el estado de realización de la tarea por parte del usuario.

        Args:
            realizado (bool): True si fue realizada, False si no.
        """
        if self.__usuario_tarea.Disponible is False:
            raise Exception("No se tiene permisos para checkear la tarea.")
        if self.__tarea.type_check is True:
            usuario_tareas = session.query(UsuarioTarea).filter_by(IDTarea=self.__usuario_tarea.IDTarea,
                                                                   IDGrupo=self.__usuario_tarea.IDGrupo).all()
            for usuario_tarea in usuario_tareas:
                usuario_tarea.Realizado = realizado

        self.__usuario_tarea.Realizado = realizado

    def update_type_check(self, type_check):
        """
        actualiza el tipo de check
        :param type_check:
        :return:
        """
        self.__tarea.type_check = type_check

    def update_detalle(self, detalle):
        """
        Actualiza el detalle o descripción de la tarea.

        Args:
            detalle (str): Nuevo detalle de la tarea.
        """
        self.__tarea.Detalle = detalle
