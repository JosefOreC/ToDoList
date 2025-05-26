"""
    Clase que representa la relación muchos a muchos de Usuarios y Grupos

"""

from base.declarative_base import Base
from sqlalchemy import Integer, ForeignKey, Column, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from rol import Rol

class UsuarioGrupo(Base):
    __tablename__ = 'USUARIO_GRUPO'

    IDUsuario = Column(Integer, ForeignKey('USUARIO.IDUsuario'), primary_key=True)
    IDGrupo = Column(Integer, ForeignKey('GRUPO.IDGrupo'), primary_key=True)
    rol = Column(Enum(Rol), nullable=False)

    usuario = relationship('Usuario', back_populates='grupos_relacion')
    grupo = relationship('Grupo', back_populates='usuarios_relacion')


if __name__ == '__main__':
    pass
