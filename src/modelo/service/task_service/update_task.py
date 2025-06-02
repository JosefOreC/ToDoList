"""
    Controla los datos de una tarea para su actualización
    no se involucra con la base de datos.
"""

from src.modelo.entities.usuario_tarea import UsuarioTarea
from src.modelo.entities.tarea import Tarea
from src.modelo.database_management.base.declarative_base import session

class UpdateTask:
    def __init__(self, id_tarea, id_usuario):
        self.id_tarea = id_tarea
        self.id_usuario = id_usuario
        self.__recover_tarea()


    def __recover_tarea(self):
        self.__tarea = session.query(Tarea).filter_by(IDTarea=self.id_tarea).first()
        self.__usuario_tarea = session.query(UsuarioTarea).filter_by(IDTarea = self.id_tarea,
                                                               IDUsuario = self.id_usuario).first()

    def update_name(self, nombre):
        self.__tarea.Nombre = nombre

    def update_activo(self, activo):
        self.__tarea.Activo = activo

    def update_fecha(self, fecha):
        self.__tarea.Fecha_programada = fecha

    def update_prioridad(self, prioridad):
        self.__tarea.Prioridad = prioridad

    def update_disponible(self, disponible):
        self.__usuario_tarea.Disponible = disponible

    def update_realizado(self, realizado):
        self.__usuario_tarea.Realizado = realizado

    def update_detalle(self, detalle):
        self.__tarea.Detalle = detalle


