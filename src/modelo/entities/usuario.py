"""
    Crea la super clase Usuario
    define los metodos de la actualizacion de datos básicos
    para las subclases Operador e Integrante
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker

from base.declarative_base import Base, engine




class Usuario(Base):
    """
        Clase usuario
        representación de la entidad USUARIO de la base de datos
    """

    __tablename__ = 'USUARIO'

    IDUsuario = Column(Integer, primary_key=True)
    Nombres = Column(String(60), nullable=False)
    Apellidos = Column(String(60), nullable=False)
    Alias = Column(String(30), nullable=False)
    Estado = Column(Integer, nullable=False)
    Password = Column(String(24))

    grupos_relacion = relationship('Grupo', back_populates='usuario')

    grupos_master = relationship('Grupo', back_populates='master', foreign_keys='Grupo.IDMaster')



if __name__ == "__main__":
    pass


