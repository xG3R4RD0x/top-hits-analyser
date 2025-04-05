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
            print("MockController: Volviendo al menú principal")
else:
    # Importaciones normales cuando se importa como módulo
    from app.view.base_view import BaseView

class DatabaseView(BaseView):
    """Vista para mostrar y gestionar la base de datos"""
    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(self, text="Base de Datos", font=("Helvetica", 14))
        self.view_label.pack(pady=10)
        
        # Frame para la tabla y controles
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        
        # Crear un Treeview para mostrar los datos
        self.create_treeview()
        
        # Botones de acción
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)
        
        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Volver al Menú Principal",
            command=lambda: self.controller.show_main_menu()
        )
        self.back_button.pack(side="left", padx=5)
        
        self.refresh_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar Datos",
            command=self.refresh_data
        )
        self.refresh_button.pack(side="right", padx=5)
    
    def create_treeview(self):
        """Crear un Treeview para mostrar los datos de las canciones"""
        columns = ("playlist", "name", "artist", "album", "release_date", "youtube_url")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        # Definir las cabeceras
        self.tree.heading("playlist", text="Playlist")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("artist", text="Artista")
        self.tree.heading("album", text="Álbum")
        self.tree.heading("release_date", text="Fecha")
        self.tree.heading("youtube_url", text="URL YouTube")
        
        # Configurar anchos de columnas
        self.tree.column("playlist", width=150)
        self.tree.column("name", width=200)
        self.tree.column("artist", width=200)
        self.tree.column("album", width=150)
        self.tree.column("release_date", width=100)
        self.tree.column("youtube_url", width=250)
        
        # Agregar scrollbars
        self.vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.content_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        # Posicionar los elementos
        self.tree.grid(column=0, row=0, sticky='nsew')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')
        
        # Configurar el grid para expandirse correctamente
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Agregar datos de muestra
        self.add_sample_data()
    
    def add_sample_data(self):
        """Añadir datos de muestra para depuración"""
        sample_data = [
            ("Reggaeton Hits", "Hawái", "Maluma", "Papi Juancho", "2020-08-21", "https://youtube.com/watch?v=123"),
            ("Top Hits", "Blinding Lights", "The Weeknd", "After Hours", "2020-03-20", "https://youtube.com/watch?v=456"),
            ("Mansion Reggaeton", "Safaera", "Bad Bunny", "YHLQMDLG", "2020-02-29", "https://youtube.com/watch?v=789"),
            ("Fiesta Mix", "Gasolina", "Daddy Yankee", "Barrio Fino", "2004-07-13", "https://youtube.com/watch?v=abc"),
            ("Reggaeton Clásicos", "Rakata", "Wisin & Yandel", "Pa'l Mundo", "2005-11-08", "https://youtube.com/watch?v=def"),
        ]
        
        for i, (playlist, name, artist, album, date, url) in enumerate(sample_data):
            self.tree.insert('', 'end', iid=i, values=(playlist, name, artist, album, date, url))
    
    def refresh_data(self):
        # Para fines de demostración, limpiamos y añadimos datos de muestra
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.add_sample_data()
        print("Datos actualizados")


# Ejecutar la vista de forma independiente cuando se ejecuta directamente
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Base de Datos - Modo Independiente")
    root.geometry("1000x600")
    
    # Configurar estilo
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    
    # Instanciar el controlador simulado y la vista
    controller = MockController()
    view = DatabaseView(root, controller)
    view.pack(fill="both", expand=True)
    
    # Ejecutar la aplicación
    root.mainloop()
