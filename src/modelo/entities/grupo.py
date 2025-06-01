"""
    Clase que representa a la entidad Grupo de la base de datos

"""
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


from src.modelo.database_management.base.declarative_base import Base


class Grupo(Base):
    __tablename__ = 'Grupo'


    IDGrupo = Column(Integer, primary_key=True)
    Nombre = Column(String(50), nullable=False)
    Fecha_creacion = Column(DATETIME)
    Descripcion = Column(String(150))

    IDMaster = Column(Integer, ForeignKey('Usuario.IDUsuario'))
    master = relationship('Usuario', back_populates='grupos_master', foreign_keys=[IDMaster])

    usuarios_relacion = relationship('UsuarioGrupo', back_populates='grupo')

    grupo_tareas = relationship('UsuarioTarea', back_populates='grupo')
    __table_args__ = (
        UniqueConstraint('Nombre', 'IDMaster', name='uq_nombre_master'),
    )

if __name__ == '__main__':
    pass