import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

# Configuración del sistema para añadir el directorio base al sys.path
# Esto permite importar módulos desde un directorio padre.
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

# Importación de módulos personalizados para el controlador y manejo de datos
from controller.controller import Controller
from model.model import guardar_tareas_en_archivo, cargar_tareas_desde_archivo

# Textos para reutilización
text1= "Descripción"
text2= "Título"
text3= "Éxito"

class GestionTareasApp:
    """Clase que representa la aplicación de gestión de tareas con una interfaz gráfica."""
    def __init__(self, root):
        # Inicialización del controlador para gestionar la lógica del negocio
        self.controller = Controller()
        self.root = root
        
        # Configuración de la ventana principal
        self.root.title("Gestión de Tareas")
        self.root.geometry("800x400")
        self.root.config(bg="#f5f5f5")

        # Cargar tareas desde el archivo
        cargar_tareas_desde_archivo()

        # Creación de la interfaz para añadir nuevas tareas
        self.form_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.form_frame.pack(pady=10)

        # Campo de entrada para el título de la tarea
        self.titulo_label = tk.Label(self.form_frame, text="Título:", bg="#f5f5f5", font=("Helvetica", 12))
        self.titulo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.titulo_entry = tk.Entry(self.form_frame, font=("Helvetica", 12))
        self.titulo_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Campo de entrada para la descripción de la tarea
        self.descripcion_label = tk.Label(self.form_frame, text="Descripción", bg="#f5f5f5", font=("Helvetica", 12))
        self.descripcion_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.descripcion_entry = tk.Entry(self.form_frame, font=("Helvetica", 12))
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Botón de agregar tarea
        self.agregar_button = tk.Button(
            self.form_frame, text="Agregar Tarea", command=self.agregar_tarea, bg="red", fg="#f5f5f5", font=("Helvetica", 12)
        )
        self.agregar_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Marco para mostrar las tareas
        self.tareas_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.tareas_frame.pack(fill="both", padx=10, pady=10)

        # Lista de tareas con Treeview
        self.tree = ttk.Treeview(self.tareas_frame, columns=("ID", text2, text1, "Estado"), show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # Definición de encabezados y columnas en la tabla de tareas
        self.tree.heading("ID", text="ID")
        self.tree.heading(text2, text=text2)
        self.tree.heading(text1, text=text1)
        self.tree.heading("Estado", text="Estado")
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column(text2, width=150, anchor="w")
        self.tree.column(text1, width=200, anchor="w")
        self.tree.column("Estado", width=100, anchor="center")

        # Cargar las tareas al iniciar la app
        self.actualizar_tareas()

        # Enlace para manejar el clic en una tarea de la lista
        self.tree.bind("<ButtonRelease-1>", self.on_tarea_click)

    def agregar_tarea(self):
        """Agrega una nueva tarea utilizando los datos del formulario."""
        titulo = self.titulo_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()

        if not titulo:
            messagebox.showerror("Error", "El título no puede estar vacío.")
            return

        # Llamamos al controlador para agregar la tarea
        tarea_agregada = self.controller.agregar_tarea(titulo, descripcion)

        if tarea_agregada:
            guardar_tareas_en_archivo()
            self.actualizar_tareas()

            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            messagebox.showinfo(text3, "Tarea agregada correctamente.")
        else:
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            # Si la tarea no se agregó, significa que el título ya existe
            messagebox.showerror("Error", "Ya existe una tarea con ese título.")

    def actualizar_tareas(self):
        """Actualiza la lista de tareas mostradas en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        tareas = self.controller.listar_tareas()

        if not tareas:
            messagebox.showinfo("Información", "No hay tareas disponibles.")
            return

        for tarea in tareas:
            tarea_id = tarea["id"]
            titulo = tarea["titulo"]
            descripcion = tarea["descripcion"]
            estado = "Completada" if tarea["completada"] else "Pendiente"
            self.tree.insert("", "end", values=(tarea_id, titulo, descripcion, estado))

    def on_tarea_click(self, event):
        """Muestra opciones al hacer clic en una tarea."""
        item = self.tree.selection()
        if not item:
            return

        tarea_id = self.tree.item(item, "values")[0]
        try:
            tarea_id = int(tarea_id)
        except ValueError:
            return

        tarea = self.controller.obtener_tarea_por_id(tarea_id)
        if tarea is None:
            messagebox.showerror("Error", "No se pudo encontrar la tarea.")
            return

        if tarea["completada"]:
            self.mostrar_boton_eliminar(tarea_id)
        else:
            self.mostrar_botones_editar_completar(tarea_id)

    def mostrar_botones_editar_completar(self, tarea_id):
        """Muestra campos para editar una tarea."""
        top = tk.Toplevel(self.root)
        top.title("Acciones de Tarea")
        top.geometry("300x150")

        tk.Button(top, text="Modificar Tarea", command=lambda: self.modificar_tarea(tarea_id, top)).pack(pady=10)
        tk.Button(top, text="Completar Tarea", command=lambda: self.completar_tarea(tarea_id, top)).pack(pady=10)

    def modificar_tarea(self, tarea_id, top):
        """Modifica la tarea con los datos deseados."""
        tarea = self.controller.obtener_tarea_por_id(tarea_id)

        nuevo_titulo = simpledialog.askstring("Modificar Título", "Nuevo Título:", initialvalue=tarea["titulo"])
        if not nuevo_titulo:
            messagebox.showerror("Error", "El título no puede estar vacío.")
            return

        nueva_descripcion = simpledialog.askstring("Modificar Descripción", "Nueva Descripción:", initialvalue=tarea["descripcion"])
        if nueva_descripcion is None:
            nueva_descripcion = tarea["descripcion"]

        self.controller.modificar_tarea(tarea_id, nuevo_titulo, nueva_descripcion)
        guardar_tareas_en_archivo()
        self.actualizar_tareas()
        top.destroy()
        messagebox.showinfo(text3, "Tarea modificada correctamente.")

    def completar_tarea(self, tarea_id, top):
        """Marca la tarea como completada."""
        self.controller.marcar_completada(tarea_id)
        guardar_tareas_en_archivo()
        self.actualizar_tareas()
        top.destroy()
        messagebox.showinfo(text3, "Tarea completada.")

    def mostrar_boton_eliminar(self, tarea_id):
        """Muestra el boton para eliminar una tarea completada"""
        top = tk.Toplevel(self.root)
        top.title("Eliminar Tarea Completada")
        top.geometry("300x150")

        tk.Button(top, text="Eliminar Tarea Completada", command=lambda: self.eliminar_tarea_completada(tarea_id, top)).pack(pady=10)

    def eliminar_tarea_completada(self, tarea_id, top):
        """Realiza la eliminacion de la tarea completada"""
        self.controller.eliminar_tareas_completadas(tarea_id)
        guardar_tareas_en_archivo()
        self.actualizar_tareas()
        top.destroy()
        messagebox.showinfo(text3, "Tarea eliminada.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GestionTareasApp(root)
    root.mainloop()
