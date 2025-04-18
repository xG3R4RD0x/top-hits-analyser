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
        def show_main_menu(self):
            print("MockController: Volviendo al menú principal")

else:
    # Importaciones normales cuando se importa como módulo
    from app.view.base_view import BaseView


class UpdateDBView(BaseView):
    """Vista para mostrar el progreso de actualización de la base de datos"""

    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(
            self, text="Actualización de Base de Datos", font=("Helvetica", 14)
        )
        self.view_label.pack(pady=10)

        # Contenedor principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para la barra de progreso
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill="x", pady=10)

        self.progress_label = ttk.Label(self.progress_frame, text="Progreso:")
        self.progress_label.pack(side="left", padx=5)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, length=500, mode="determinate", orient="horizontal"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        self.progress_percentage = ttk.Label(self.progress_frame, text="0%")
        self.progress_percentage.pack(side="left", padx=5)

        # Frame para el log
        self.log_frame = ttk.Frame(self.main_frame)
        self.log_frame.pack(fill="both", expand=True, pady=10)

        self.log_label = ttk.Label(self.log_frame, text="Log de Operaciones:")
        self.log_label.pack(anchor="w")

        # Crear un widget Text con scrollbar para el log
        self.log_text_frame = ttk.Frame(self.log_frame)
        self.log_text_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(self.log_text_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(side="left", fill="both", expand=True)

        self.log_scrollbar = ttk.Scrollbar(
            self.log_text_frame, command=self.log_text.yview
        )
        self.log_scrollbar.pack(side="right", fill="y")

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.log_text.configure(
            state="disabled"
        )  # Inicialmente deshabilitado para evitar edición

        # Botones de acción
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)

        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Volver al Menú Principal",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=10)

        self.cancel_button = ttk.Button(
            self.buttons_frame, text="Cancelar Operación", command=self.cancel_operation
        )
        self.cancel_button.pack(side="right", padx=10)

        # Estado inicial
        self.is_operation_running = False
        self.cancelled = False

    def go_to_main_menu(self):
        """Volver al menú principal"""
        self.trigger_event("navigate_to", "main_menu")

    def update_progress(self, value, text=None):
        """
        Actualiza la barra de progreso y opcionalmente el texto de porcentaje

        Args:
            value: Valor de progreso (0-100)
            text: Texto opcional para mostrar (si es None, se muestra el porcentaje)
        """
        self.progress_bar["value"] = value

        if text is None:
            self.progress_percentage["text"] = f"{int(value)}%"
        else:
            self.progress_percentage["text"] = text

        # Forzar actualización de la UI
        self.update_idletasks()

    def add_log_message(self, message):
        """
        Añade un mensaje al área de log

        Args:
            message: Mensaje a añadir
        """
        # Habilitar el widget Text para edición
        self.log_text.configure(state="normal")

        # Añadir mensaje con salto de línea
        self.log_text.insert(tk.END, f"{message}\n")

        # Desplazar automáticamente al final del texto
        self.log_text.see(tk.END)

        # Deshabilitar de nuevo para evitar edición manual
        self.log_text.configure(state="disabled")

        # Forzar actualización de la UI
        self.update_idletasks()

    def start_operation(self):
        """Iniciar la operación de actualización"""
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.back_button["state"] = "disabled"

        # Limpiar el log
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        # Reiniciar la barra de progreso
        self.update_progress(0)

        # Añadir un mensaje inicial
        self.add_log_message("Iniciando actualización de la base de datos...")

    def complete_operation(self, success=True):
        """Finalizar la operación"""
        self.is_operation_running = False
        self.cancel_button["state"] = "disabled"
        self.back_button["state"] = "normal"

        if success:
            self.update_progress(100, "Completado")
            self.add_log_message("Operación completada con éxito.")
        else:
            if self.cancelled:
                self.add_log_message("Operación cancelada por el usuario.")
            else:
                self.add_log_message("La operación falló. Revise los detalles arriba.")

    def cancel_operation(self):
        """Cancelar la operación en curso"""
        self.trigger_event("cancel_update_operation")


# Código para depuración y prueba independiente
if __name__ == "__main__":
    import time
    import threading

    root = tk.Tk()
    root.title("Actualización de Base de Datos - Modo Independiente")
    root.geometry("700x500")

    # Configurar estilo
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")

    # Instanciar el controlador simulado y la vista
    controller = MockController()
    view = UpdateDBView(root, controller)
    view.pack(fill="both", expand=True)

    # Función para simular un proceso de actualización
    def simulate_update_process():
        view.start_operation()

        steps = [
            "Conectando con Spotify API...",
            "Recuperando listas de reproducción...",
            "Descargando información de canciones...",
            "Buscando URLs de YouTube...",
            "Actualizando base de datos...",
            "Guardando resultados...",
        ]

        progress_per_step = 100 / len(steps)
        current_progress = 0

        for step in steps:
            if view.cancelled:
                break

            view.add_log_message(step)
            current_progress += progress_per_step / 2
            view.update_progress(current_progress)

            # Simular tiempo de procesamiento
            time.sleep(1)

            # Simular progreso dentro del paso
            for i in range(10):
                if view.cancelled:
                    break
                time.sleep(0.1)
                current_progress += progress_per_step / 20
                view.update_progress(current_progress)

            view.add_log_message(f"✓ {step} completado")

        # Finalizar la operación
        if not view.cancelled:
            view.complete_operation(True)

    # Botón para iniciar la simulación
    start_button = ttk.Button(
        root,
        text="Iniciar Simulación",
        command=lambda: threading.Thread(
            target=simulate_update_process, daemon=True
        ).start(),
    )
    start_button.pack(pady=10)

    root.mainloop()
