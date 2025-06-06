from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.modelo.database_management.base.declarative_base import Base
from src.modelo.entities.modelo import Usuario  # Ajusta según tu estructura real


# Definir ruta de la base de datos

engine = create_engine(f'sqlite:///database.db', echo=True)

# Crear todas las tablas definidas en Base (incluyendo Usuario)
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()


print("Base de datos creada.")