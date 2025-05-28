from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurar base de datos SQLite en memoria para las pruebas
engine = create_engine('sqlite:///D://Python//todolist_first_try//src//modelo//entities//database.db', echo=False)
# engine = create_engine('sqlite:///', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()

# Crear la base de datos en memoria
#engine = create_engine('sqlite:///:memory:')
#Base.metadata.create_all(engine)
#Session = sessionmaker(bind=engine)