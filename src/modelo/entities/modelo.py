import enum
from base.declarative_base import Base, engine
from sqlalchemy import Column, String, Integer, ForeignKey, DATE, Enum
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from usuario_grupo import UsuarioGrupo
from usuario import Usuario
from grupo import Grupo
from rol import Rol
from tarea import Tarea
from usuario_tarea import UsuarioTarea


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

    fecha = datetime(day=27, month=5, year=2025).date()

    tarea = Tarea(Nombre='Hacer los test', Fecha_programada=fecha, Prioridad=1)

    session.add_all([tarea])
    session.commit()

    rel1 = UsuarioTarea(IDUsuario=1, IDGrupo=1, IDTarea=tarea.IDTarea)
    session.add_all([rel1])
    session.commit()