from model.model import agregar_tarea, listar_tareas, marcar_completada, eliminar_tarea, modificar_tarea

class Controller:
    def agregar_tarea(self, titulo, descripcion):
        """
        Agrega una nueva tarea con el título y descripción proporcionados.
        Retorna True si se agregó exitosamente, False si ya existe un título igual.
        """
        if not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")
        return agregar_tarea(titulo, descripcion)

    def listar_tareas(self):
        """
        Retorna una lista de todas las tareas almacenadas en la base de datos.
        """
        try:
            return listar_tareas()
        except Exception as e:
            print(f"Error al listar tareas: {e}")
            return []

    def marcar_completada(self, id_tarea):
        """
        Marca como completada una tarea por su ID.
        Retorna True si se marcó exitosamente, "Ya completada" si ya lo estaba, o False si no se encontró.
        """
        if not isinstance(id_tarea, int):
            raise ValueError("El ID de la tarea debe ser un número entero.")
        return marcar_completada(id_tarea)

    def eliminar_tareas_completadas(self, tarea_id):
        """
        Elimina una tarea específica si está marcada como completada.
        """
        try:
            return eliminar_tarea(tarea_id)
        except Exception as e:
            print(f"Error al eliminar tareas completadas: {e}")

    def obtener_tarea_por_id(self, id_tarea):
        """
        Busca y retorna una tarea por su ID.
        Retorna None si no se encuentra.
        """
        if not isinstance(id_tarea, int):
            raise ValueError("El ID de la tarea debe ser un número entero.")
        tareas = listar_tareas()
        for tarea in tareas:
            if tarea["id"] == id_tarea:
                return tarea
        return None

    def modificar_tarea(self, tarea_id, nuevo_titulo, nueva_descripcion):
        """
        Modifica el título y la descripción de una tarea existente por su ID.
        """
        if not nuevo_titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        return modificar_tarea(tarea_id, nuevo_titulo, nueva_descripcion)
