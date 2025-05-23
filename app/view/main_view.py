import tkinter as tk
from tkinter import ttk

# Importar las vistas separadas
from app.view.menu_view import MainMenuView
from app.view.database_view import DatabaseView
from app.view.update_db_view import UpdateDBView


class MainView:
    """
    Clase principal que actúa como contenedor y gestor de frames/vistas de la aplicación.
    Permite cambiar dinámicamente entre diferentes vistas manteniendo la estructura principal.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Hits Downloader")
        self.root.geometry("800x600")

        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure(
            "Header.TLabel", font=("Helvetica", 16, "bold"), background="#f0f0f0"
        )

        # Crear el contenedor principal
        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(side="top", fill="both", expand=True)

        # Crear el header que será consistente en todas las vistas
        self.header = ttk.Frame(self.main_container, style="TFrame")
        self.header.pack(side="top", fill="x", padx=10, pady=10)

        self.title_label = ttk.Label(
            self.header, text="Hits Downloader", style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=10)

        # Crear el contenedor para las vistas (frames) que irán cambiando
        self.content_container = ttk.Frame(self.main_container, style="TFrame")
        self.content_container.pack(
            side="top", fill="both", expand=True, padx=10, pady=10
        )

        # Crear el footer para navegación y controles comunes
        self.footer = ttk.Frame(self.main_container, style="TFrame")
        self.footer.pack(side="bottom", fill="x", padx=10, pady=10)

        # Diccionario para almacenar todas las vistas/frames
        self.frames = {}

    def add_frame(self, frame_class, frame_name, *args, **kwargs):
        """
        Añade un nuevo frame al gestor de vistas.

        Args:
            frame_class: La clase del frame a crear
            frame_name: Nombre/identificador único para el frame
            *args, **kwargs: Argumentos adicionales para el constructor del frame
        """
        frame = frame_class(self.content_container, *args, **kwargs)
        self.frames[frame_name] = frame
        frame.pack_forget()  # No mostrar inmediatamente

        return frame

    def show_frame(self, frame_name):
        """
        Muestra el frame especificado y oculta los demás.

        Args:
            frame_name: Nombre/identificador del frame a mostrar
        """
        # Verificar si el frame existe
        if frame_name not in self.frames:
            print(
                f"Error: No se puede mostrar el frame '{frame_name}' porque no existe."
            )
            return

        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Mostrar el frame solicitado
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    main_view = MainView(root)
    root.mainloop()
