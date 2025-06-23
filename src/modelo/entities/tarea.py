"""
    Crea la clase tarea que maneja los datos de las tareas
    que el usuario maneja.
"""


from sqlalchemy import Column, Boolean, String, Integer, DATE
from sqlalchemy.orm import relationship

from src.modelo.database_management.base.declarative_base import Base

class Tarea(Base):
    __tablename__ = "Tarea"

    IDTarea = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    Activo = Column(Boolean, default=True)
    Fecha_programada = Column(DATE)
    Prioridad = Column(Integer)
    Detalle = Column(String(500))
    """
        Tipo de checkeo - individual - no individual
    """
    type_check = Column(Boolean, default=False) # False: Individual, True: Grupal

    tarea_usuarios = relationship('UsuarioTarea', back_populates='tarea')

if __name__ == '__main__':
    pass