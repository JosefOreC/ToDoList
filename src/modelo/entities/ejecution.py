from base.declarative_base import Base, engine
from sqlalchemy.orm import sessionmaker
from grupo import Grupo
from usuario import Usuario
from rol import Rol
from usuario_grupo_model import UsuarioGrupo
from datetime import datetime

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

usuario = Usuario(Nombres='Josef Pablo', Apellidos = 'Oré Campos',
                  Alias = 'JosefOre', Estado = 1, Password = 'cisco')
fecha = datetime.strptime('26-05-2025', '%d-%m-%Y').date()

session.add_all([usuario])
session.commit()

grupo = Grupo(Nombre = 'Wasaverto', Fecha_Creacion = fecha,
              Descripcion = 'SE NOS FUE DE LAS MANOS',
              IDMaster = usuario.IDUsuario)

session.add_all([grupo])

rel1 = UsuarioGrupo(usuario=usuario, grupo=grupo, rol = Rol.master)
session.add_all([rel1])
session.commit()

for rel in session.query(Usuario).all():
    print(rel.Nombres)