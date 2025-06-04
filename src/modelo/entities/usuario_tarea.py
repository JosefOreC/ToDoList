"""
    Crea la tabla intermedia entre Usuario y Tarea
"""
from sqlalchemy.orm import relationship

from src.modelo.database_management.base.declarative_base import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean

class UsuarioTarea(Base):
    __tablename__ = 'UsuarioTarea'
    IDUsuario = Column(Integer, ForeignKey('Usuario.IDUsuario'), primary_key=True)
    IDTarea = Column(Integer, ForeignKey('Tarea.IDTarea'), primary_key=True)
    IDGrupo = Column(Integer, ForeignKey('Grupo.IDGrupo'), nullable=True)

    Disponible = Column(Boolean, default=True)
    Realizado = Column(Boolean, default=False)
    Archivado = Column(Boolean, default=False)

    grupo = relationship('Grupo', back_populates='grupo_tareas')
    tarea = relationship('Tarea', back_populates='tarea_usuarios')
    usuario = relationship('Usuario', back_populates='usuario_tareas')

