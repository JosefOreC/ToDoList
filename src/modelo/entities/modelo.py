import enum
from base.declarative_base import Base, engine
from sqlalchemy import Column, String, Integer, ForeignKey, DATE, Enum
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
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
    Estado = Column(Integer, nullable=False)
    Password = Column(String(24))

    grupos_relacion = relationship('UsuarioGrupo', back_populates='usuario')

    grupos_master = relationship('Grupo', back_populates='master', foreign_keys='Grupo.IDMaster')


class Rol(enum.Enum):
    master = 'master'
    editor = 'editor'
    miembro = 'miembro'

class Grupo(Base):
    __tablename__ = 'Grupo'


    IDGrupo = Column(Integer, primary_key=True)
    Nombre = Column(String(50), nullable=False)
    Fecha_Creacion = Column(DATE)
    Descripcion = Column(String(150))

    IDMaster = Column(Integer, ForeignKey('Usuario.IDUsuario'))
    master = relationship('Usuario', back_populates='grupos_master', foreign_keys=[IDMaster])

    usuarios_relacion = relationship('UsuarioGrupo', back_populates='grupo')

class UsuarioGrupo(Base):
    __tablename__ = 'UsuarioGrupo'

    IDUsuario = Column(Integer, ForeignKey('Usuario.IDUsuario'), primary_key=True)
    IDGrupo = Column(Integer, ForeignKey('Grupo.IDGrupo'), primary_key=True)
    rol = Column(Enum(Rol), nullable=False)
    usuario = relationship('Usuario', back_populates='grupos_relacion')
    grupo = relationship('Grupo', back_populates='usuarios_relacion')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    usuario = Usuario(Nombres='Carlos Alberto', Apellidos='Tovar',
                      Alias='Beto', Estado=1, Password='Cisco')


    session.add_all([usuario])
    session.commit()
    fecha = datetime.strptime('17-03-2025', '%d-%m-%Y').date()
    grupo = Grupo(Nombre='Wasaverto', Fecha_Creacion=fecha,
                  Descripcion='SE NOS FUE DE LAS MANOS',
                  IDMaster=usuario.IDUsuario)
    session.add_all([grupo])
    rel1 = UsuarioGrupo(usuario=usuario, grupo=grupo, rol=Rol.master)
    session.add_all([rel1])
    session.commit()

    for rel in session.query(Usuario):
        print()