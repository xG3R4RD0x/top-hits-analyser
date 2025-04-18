import tkinter as tk
from tkinter import ttk


class BaseView(ttk.Frame):
    """Clase base para todas las vistas/frames de la aplicación."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self._event_handlers = {}

        # Configuración común para todos los frames
        self.configure(style="TFrame", padding="10")

        # Cada subclase debe implementar su propia interfaz
        self.setup_ui()

    def setup_ui(self):
        """Método que cada subclase debe implementar para configurar su UI."""
        raise NotImplementedError("Las subclases deben implementar este método")

    def register_event_handler(self, event_name, handler):
        """Registra un manejador para un evento específico."""
        self._event_handlers[event_name] = handler

    def trigger_event(self, event_name, *args, **kwargs):
        """Dispara un evento con los argumentos proporcionados."""
        if event_name in self._event_handlers:
            return self._event_handlers[event_name](*args, **kwargs)
        else:
            print(
                f"Advertencia: No hay manejador registrado para el evento '{event_name}'"
            )
