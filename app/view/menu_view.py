import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajuste especial para importaciones cuando se ejecuta directamente
if __name__ == "__main__":
    # Obtener la ruta absoluta al directorio raíz del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Añadir el directorio raíz al path de Python
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    # Importaciones directas para ejecución independiente
    from app.view.base_view import BaseView
    
    # Crear un controlador simulado para pruebas
    class MockController:
        def show_main_menu(self):
            print("MockController: Mostrando menú principal")
            
        def show_database_view(self):
            print("MockController: Mostrando vista de base de datos")
            
        def show_download_view(self):
            print("MockController: Mostrando vista de descarga")
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
            command=self.update_and_download
        )
        self.update_and_download_button.pack(fill="x", pady=5)
        
        self.check_database_button = ttk.Button(
            self.buttons_frame, 
            text="Revisar base de datos actual",
            command=self.check_database
        )
        self.check_database_button.pack(fill="x", pady=5)
        
        self.update_database_button = ttk.Button(
            self.buttons_frame, 
            text="Actualizar base de datos",
            command=self.update_database
        )
        self.update_database_button.pack(fill="x", pady=5)
        
        self.download_with_database_button = ttk.Button(
            self.buttons_frame, 
            text="Descargar canciones con base de datos actual",
            command=self.download_with_database
        )
        self.download_with_database_button.pack(fill="x", pady=5)
        
        self.view_database_button = ttk.Button(
            self.buttons_frame, 
            text="Ver base de datos",
            command=self.view_database
        )
        self.view_database_button.pack(fill="x", pady=5)
    
    def update_and_download(self):
        if hasattr(self, "commands") and "update_and_download" in self.commands:
            self.commands["update_and_download"]()
    
    def check_database(self):
        if hasattr(self, "commands") and "check_database" in self.commands:
            self.commands["check_database"]()
    
    def update_database(self):
        if hasattr(self, "commands") and "update_database" in self.commands:
            self.commands["update_database"]()
    
    def download_with_database(self):
        if hasattr(self, "commands") and "download_with_database" in self.commands:
            self.commands["download_with_database"]()
            # Cambiar a la vista de descarga
            self.controller.show_download_view()
    
    def view_database(self):
        if hasattr(self, "commands") and "view_database" in self.commands:
            self.commands["view_database"]()
            # Cambiar a la vista de base de datos
            self.controller.show_database_view()


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
    
    # Configurar comandos simulados para probar
    view.set_commands({
        "update_and_download": lambda: print("Simulación: Actualizar y descargar"),
        "check_database": lambda: print("Simulación: Verificar base de datos"),
        "update_database": lambda: print("Simulación: Actualizar base de datos"),
        "download_with_database": lambda: print("Simulación: Descargar con base de datos"),
        "view_database": lambda: print("Simulación: Ver base de datos"),
    })
    
    # Ejecutar la aplicación
    root.mainloop()
