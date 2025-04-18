import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajuste especial para importaciones cuando se ejecuta directamente
if __name__ == "__main__":
    # Obtener la ruta absoluta al directorio raíz del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Añadir el directorio raíz al path de Python
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Importaciones directas para ejecución independiente
    from app.view.base_view import BaseView

    # Crear un controlador simulado para pruebas
    class MockController:
        def handle_action(self, action_name):
            print(f"MockController: Acción '{action_name}' ejecutada.")

else:
    # Importaciones normales cuando se importa como módulo
    from app.view.base_view import BaseView


class MainMenuView(BaseView):
    """Vista del menú principal"""

    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(self, text="Menú Principal", font=("Helvetica", 14))
        self.view_label.pack(pady=10)

        # Frame para los botones
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="both", expand=True)

        # Botones
        self.update_and_download_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar base de datos y descargar canciones",
            command=self.update_and_download,
        )
        self.update_and_download_button.pack(fill="x", pady=5)

        self.check_database_button = ttk.Button(
            self.buttons_frame,
            text="Revisar base de datos actual",
            command=self.check_database,
        )
        self.check_database_button.pack(fill="x", pady=5)

        self.update_database_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar base de datos",
            command=self.update_songs_database,
        )
        self.update_database_button.pack(fill="x", pady=5)

        self.download_with_database_button = ttk.Button(
            self.buttons_frame,
            text="Descargar canciones con base de datos actual",
            command=self.download_with_database,
        )
        self.download_with_database_button.pack(fill="x", pady=5)

        self.view_database_button = ttk.Button(
            self.buttons_frame,
            text="Ver base de datos",
            command=self.view_database,
        )
        self.view_database_button.pack(fill="x", pady=5)

    def update_and_download(self):
        """Handle the 'Actualizar base de datos y descargar canciones' action."""
        self.controller.handle_action("update_and_download")

    def check_database(self):
        """Handle the 'Revisar base de datos actual' action."""
        self.controller.handle_action("check_database")

    def update_songs_database(self):
        """Handle the 'Actualizar base de datos' action."""
        self.controller.handle_action("update_songs_database")

    def download_with_database(self):
        """Handle the 'Descargar canciones con base de datos actual' action."""
        self.controller.handle_action("download_with_database")

    def view_database(self):
        """Handle the 'Ver base de datos' action."""
        self.controller.handle_action("view_database")


# Ejecutar la vista de forma independiente cuando se ejecuta directamente
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menú Principal - Modo Independiente")
    root.geometry("800x600")

    # Configurar estilo
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")

    # Instanciar el controlador simulado y la vista
    controller = MockController()
    view = MainMenuView(root, controller)
    view.pack(fill="both", expand=True)

    # Ejecutar la aplicación
    root.mainloop()
