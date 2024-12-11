import json
from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base, session, engine

TAREAS_JSON_PATH = "tareas.json"

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)

    # Permite extender la tabla si ya existe
    __table_args__ = {'extend_existing': True}

# Crear las tablas usando el engine
Base.metadata.create_all(engine)

def guardar_tareas_en_archivo(archivo=TAREAS_JSON_PATH):
    """Guarda las tareas actuales en un archivo JSON."""
    try:
        tareas = session.query(Tarea).all()
        tareas_data = [
            {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            }
            for tarea in tareas
        ]
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(tareas_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar las tareas en el archivo: {e}")

def cargar_tareas_desde_archivo(archivo=TAREAS_JSON_PATH):
    """Carga las tareas desde un archivo JSON a la base de datos."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            tareas_data = json.load(f)
            for tarea_data in tareas_data:
                tarea = session.query(Tarea).filter_by(id=tarea_data['id']).first()
                if not tarea:
                    tarea = Tarea(
                        id=tarea_data['id'],
                        titulo=tarea_data['titulo'],
                        descripcion=tarea_data['descripcion'],
                        completada=tarea_data['completada']
                    )
                    session.add(tarea)
            session.commit()
    except FileNotFoundError:
        print("Archivo JSON no encontrado. Se continuará sin cargar tareas.")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Verifica su formato.")
    except Exception as e:
        print(f"Error inesperado al cargar las tareas: {e}")

def agregar_tarea(titulo, descripcion):
    """Agrega una nueva tarea a la base de datos."""
    if session.query(Tarea).filter_by(titulo=titulo).first():
        return False  # El título ya existe
    try:
        nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
        session.add(nueva_tarea)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al agregar la tarea: {e}")
        return False

def listar_tareas():
    """Lista todas las tareas directamente desde la base de datos."""
    try:
        tareas = session.query(Tarea).all()
        return [
            {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            }
            for tarea in tareas
        ]
    except Exception as e:
        print(f"Error al listar tareas: {e}")
        return []

def marcar_completada(id_tarea):
    """Marca una tarea como completada por su ID."""
    try:
        tarea = session.query(Tarea).get(id_tarea)
        if tarea:
            if tarea.completada:
                return "Ya completada"
            tarea.completada = True
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error al marcar la tarea como completada: {e}")
        return False

def eliminar_tarea(tarea_id):
    """
    Elimina una tarea específica si está marcada como completada.
    """
    try:
        # Obtén la tarea por ID
        tarea = session.query(Tarea).get(tarea_id)
        if tarea and tarea.completada:
            session.delete(tarea)
            session.commit()
            print(f"Tarea con ID {tarea_id} eliminada.")
        else:
            print(f"No se encontró la tarea completada con ID {tarea_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar tarea completada: {e}")
        
def modificar_tarea(tarea_id, nuevo_titulo, nueva_descripcion):
    """Modifica el título y la descripción de una tarea existente."""
    try:
        tarea = session.query(Tarea).get(tarea_id)
        if tarea:
            # Actualizamos el título y la descripción
            tarea.titulo = nuevo_titulo
            tarea.descripcion = nueva_descripcion
            session.commit()
            return True
        return False  # Si no se encuentra la tarea, retornamos False
    except Exception as e:
        session.rollback()
        print(f"Error al modificar la tarea: {e}")
        return False
