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
        self.root.geometry("900x650")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure(
            "Header.TLabel", font=("Helvetica", 16, "bold"), background="#f0f0f0"
        )
        self.style.configure(
            "Nav.TButton", font=("Helvetica", 11), padding=10
        )
        self.style.configure(
            "NavSelected.TButton", font=("Helvetica", 11, "bold"), padding=10
        )

        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(side="top", fill="both", expand=True)

        self.create_sidebar()
        self.create_header()
        self.create_content_area()

        self.frames = {}
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def create_sidebar(self):
        self.sidebar = ttk.Frame(self.main_container, style="TFrame", width=200)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        self.logo_label = ttk.Label(
            self.sidebar, 
            text="🎵 Hits\nDownloader", 
            font=("Helvetica", 16, "bold"),
            background="#2c3e50",
            foreground="white",
            padding=20
        )
        self.logo_label.pack(fill="x", pady=(0, 10))

        self.nav_frame = ttk.Frame(self.sidebar, style="TFrame")
        self.nav_frame.pack(fill="x", padx=5, pady=5)

        self.nav_buttons = {}
        
        nav_items = [
            ("main_menu", "🏠 Inicio"),
            ("update_db_view", "⬇️ Descargar & Actualizar"),
            ("database_view", "📊 Ver Base de Datos"),
            ("manage_playlists_view", "📋 Gestionar Playlists"),
        ]
        
        for view_id, text in nav_items:
            btn = ttk.Button(
                self.nav_frame,
                text=text,
                style="Nav.TButton",
                command=lambda v=view_id: self.navigate_callback(v)
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[view_id] = btn

        self.current_view = "main_menu"
        self.update_nav_buttons()

    def navigate_callback(self, view_name):
        self.current_view = view_name
        self.update_nav_buttons()
        if self.controller:
            self.controller.navigate_to(view_name)

    def update_nav_buttons(self):
        for view_id, btn in self.nav_buttons.items():
            if view_id == self.current_view:
                btn.config(style="NavSelected.TButton")
            else:
                btn.config(style="Nav.TButton")

    def create_header(self):
        self.header = ttk.Frame(self.main_container, style="TFrame")
        self.header.pack(side="top", fill="x", padx=20, pady=15)

        self.title_label = ttk.Label(
            self.header, text="Menú Principal", style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=10)

    def create_content_area(self):
        self.content_container = ttk.Frame(self.main_container, style="TFrame")
        self.content_container.pack(
            side="top", fill="both", expand=True, padx=20, pady=(0, 15)
        )

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
        if frame_name not in self.frames:
            print(
                f"Error: No se puede mostrar el frame '{frame_name}' porque no existe."
            )
            return

        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        
        self.current_view = frame_name
        self.update_nav_buttons()
        self.update_title(frame_name)
        return frame

    def update_title(self, view_name):
        titles = {
            "main_menu": "Menú Principal",
            "update_db_view": "Descargar y Actualizar Base de Datos",
            "database_view": "Ver Base de Datos",
            "manage_playlists_view": "Gestión de Playlists",
        }
        self.title_label.config(text=titles.get(view_name, "Hits Downloader"))


if __name__ == "__main__":
    root = tk.Tk()
    main_view = MainView(root)
    root.mainloop()
