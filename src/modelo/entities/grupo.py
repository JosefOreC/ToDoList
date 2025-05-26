"""
    Clase que representa a la entidad Grupo de la base de datos

"""
from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from sqlalchemy.orm import Relationship, relationship


from base.declarative_base import Base


class Grupo(Base):
    __tablename__ = 'GRUPO'


    IDGrupo = Column(Integer, primary_key=True)
    Nombre = Column(String(50), nullable=False)
    Fecha_Creacion = Column(DATE)
    Descripcion = Column(String(150))

    IDMaster = Column(Integer, ForeignKey('Usuario.IDUsuario'))
    master = relationship('Usuario', back_populates='grupos_master', foreign_keys=[IDMaster])

    usuarios_relacion = relationship('UsuarioGrupo', back_populates='grupo')

if __name__ == '__main__':
    pass