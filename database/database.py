from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
Base = declarative_base()
engine = create_engine('sqlite:///tareas.db')
Session = sessionmaker(bind=engine)
session = Session()

# Modelo de Tarea
class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)

# Crear las tablas si no existen
Base.metadata.create_all(engine)
