import tkinter as tk
from tkinter import ttk
import sys
import os
import threading
import time
import random

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
        def show_main_menu(self):
            print("MockController: Volviendo al menú principal")

else:
    # Importaciones normales cuando se importa como módulo
    from app.view.base_view import BaseView


class DownloadView(BaseView):
    """Vista para mostrar y gestionar descargas"""

    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(
            self, text="Descarga de Canciones", font=("Helvetica", 14)
        )
        self.view_label.pack(pady=10)

        # Frame para la lista de descargas y progreso
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Crear lista de descargas con barras de progreso
        self.create_download_list()

        # Botones de acción
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)

        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Volver al Menú Principal",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=5)

        self.start_button = ttk.Button(
            self.buttons_frame, text="Iniciar Descarga", command=self.start_download
        )
        self.start_button.pack(side="right", padx=5)

        # Añadir descargas de muestra
        self.add_sample_downloads()

    def create_download_list(self):
        """Crear la lista de descargas con barras de progreso"""
        # Crear un frame con scrollbar
        self.download_frame = ttk.Frame(self.content_frame)
        self.download_frame.pack(fill="both", expand=True, pady=10)

        # Crear un canvas con scrollbar para la lista de descargas
        self.canvas = tk.Canvas(self.download_frame)
        scrollbar = ttk.Scrollbar(
            self.download_frame, orient="vertical", command=self.canvas.yview
        )

        # Frame interno para los elementos de descarga
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Empaquetar todo
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variable para seguir las filas de descargas
        self.download_rows = {}

    def add_download_item(self, song_name, artist, status="Pendiente"):
        """Añadir un elemento de descarga a la lista"""
        row = len(self.download_rows)

        # Crear frame para este elemento
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", padx=5, pady=5)

        # Etiqueta con nombre e info
        label = ttk.Label(
            item_frame, text=f"{song_name} - {artist}", width=30, anchor="w"
        )
        label.grid(row=0, column=0, padx=5, sticky="w")

        # Barra de progreso
        progress = ttk.Progressbar(item_frame, length=300, mode="determinate", value=0)
        progress.grid(row=0, column=1, padx=5)

        # Etiqueta de estado
        status_label = ttk.Label(item_frame, text=status, width=15)
        status_label.grid(row=0, column=2, padx=5)

        # Guardar referencias
        self.download_rows[row] = {
            "frame": item_frame,
            "label": label,
            "progress": progress,
            "status": status_label,
            "song_name": song_name,
            "artist": artist,
        }

        return row

    def update_progress(self, row_id, progress_value, status_text=None):
        """Actualizar el progreso y estado de una descarga"""
        if row_id in self.download_rows:
            self.download_rows[row_id]["progress"]["value"] = progress_value

            if status_text:
                self.download_rows[row_id]["status"]["text"] = status_text

            # Actualizar la interfaz
            self.update_idletasks()

    def add_sample_downloads(self):
        """Añadir descargas de muestra para depuración"""
        sample_songs = [
            ("Gasolina", "Daddy Yankee"),
            ("Hawái", "Maluma"),
            ("Despacito", "Luis Fonsi"),
            ("Con Calma", "Daddy Yankee"),
            ("Taki Taki", "DJ Snake"),
            ("Mi Gente", "J Balvin"),
            ("Baila Conmigo", "Selena Gomez"),
            ("Dákiti", "Bad Bunny"),
            ("La Canción", "J Balvin & Bad Bunny"),
            ("Ginza", "J Balvin"),
        ]

        for song_name, artist in sample_songs:
            self.add_download_item(song_name, artist)

    def simulate_download_progress(self, row_id):
        """Simular el progreso de descarga para depuración"""
        progress = 0
        statuses = ["Descargando", "Procesando", "Completado"]
        current_status = 0

        self.update_progress(row_id, progress, statuses[current_status])

        while progress < 100 and not getattr(self, "stop_simulation", False):
            # Simular progreso aleatorio
            progress += random.randint(1, 10)
            progress = min(progress, 100)

            # Cambiar estado a veces
            if progress > 50 and current_status == 0:
                current_status = 1

            if progress == 100:
                current_status = 2

            # Actualizar UI
            self.update_progress(row_id, progress, statuses[current_status])

            # Esperar un tiempo
            time.sleep(0.3)

    def go_to_main_menu(self):
        """Volver al menú principal"""
        self.trigger_event("navigate_to", "main_menu")

    def start_download(self):
        """Iniciar la descarga de canciones"""
        self.trigger_event("start_download")


# Ejecutar la vista de forma independiente cuando se ejecuta directamente
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Descargas - Modo Independiente")
    root.geometry("800x600")

    # Configurar estilo
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")

    # Instanciar el controlador simulado y la vista
    controller = MockController()
    view = DownloadView(root, controller)
    view.pack(fill="both", expand=True)

    # Ejecutar la aplicación
    root.mainloop()
