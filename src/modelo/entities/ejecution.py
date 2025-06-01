from src.modelo.database_management.base.declarative_base import Base, engine
from sqlalchemy.orm import sessionmaker
from usuario_tarea import UsuarioTarea
from tarea import Tarea

from datetime import datetime

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

fecha = datetime(day=27, month=5, year=2025).date()

tarea = Tarea(Nombre = 'Hacer los test', Fecha_programada = fecha, Prioridad = 1)

session.add_all([tarea])
session.commit()

rel1 = UsuarioTarea(IDUsuario = 1, IDGrupo = 1, IDTarea = tarea.IDTarea)
session.add_all([rel1])
session.commit()
