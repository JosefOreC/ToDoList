"""
    Crea la super clase Usuario
    define los metodos de la actualizacion de datos básicos
    para las subclases Operador e Integrante
"""

from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from src.modelo.database_management.base.declarative_base import Base


class Usuario(Base):
    """
        Clase usuario
        representación de la entidad USUARIO de la base de datos
    """

    __tablename__ = 'Usuario'

    IDUsuario = Column(Integer, primary_key=True)
    Nombres = Column(String(60), nullable=False)
    Apellidos = Column(String(60), nullable=False)
    Alias = Column(String(30), nullable=False)
    Estado = Column(Boolean, default=True)
    Password = Column(String(100))

    grupos_relacion = relationship('UsuarioGrupo', back_populates='usuario')

    grupos_master = relationship('Grupo', back_populates='master', foreign_keys='Grupo.IDMaster')

    usuario_tareas = relationship('UsuarioTarea', back_populates='usuario')

    __table_args__ = (
        UniqueConstraint('Alias', name='uq_alias_usuario'),
    )

if __name__ == "__main__":
    pass


