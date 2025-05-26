from base.declarative_base import Base, engine

from usuario_grupo_model import UsuarioGrupo
from grupo import Grupo
from rol import Rol
from usuario import Usuario
from sqlalchemy.orm import sessionmaker

usuario = Usuario(Nombres='Carlos Alberto', Apellidos = 'Tovar',
                  Alias = 'Beto', Estado = 1, Password = 'Cisco')

grupo = Grupo(grupo = 'Wasaverto', Fecha_Creacion = '17-03-2025',
              Descripcion = 'SE NOS FUE DE LAS MANOS',
              IDMaster = 1)




Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



session.add([usuario,grupo])
session.commit()

rel1 = UsuarioGrupo(usuario=usuario, grupo=grupo, rol = Rol.master)
session.add([rel1])
session.commit()

for rel in usuario.grupos_relacion:
    print(usuario.grupo.Nombre)