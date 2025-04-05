import tkinter as tk
from tkinter import ttk

class BaseView(ttk.Frame):
    """Clase base para todas las vistas/frames de la aplicación."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        # Configuración común para todos los frames
        self.configure(style="TFrame", padding="10")
        
        # Cada subclase debe implementar su propia interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Método que cada subclase debe implementar para configurar su UI."""
        raise NotImplementedError("Las subclases deben implementar este método")
    
    def set_commands(self, commands):
        """Configura los comandos de los botones en este frame."""
        self.commands = commands


# Ejemplo simple para probar BaseView cuando se ejecuta directamente
if __name__ == "__main__":
    # Crear una subclase de prueba
    class TestView(BaseView):
        def setup_ui(self):
            label = ttk.Label(self, text="Esta es una vista de prueba de BaseView")
            label.pack(pady=20)
            
            button = ttk.Button(self, text="Presionar", 
                               command=lambda: print("Botón presionado"))
            button.pack(pady=10)
    
    # Crear y mostrar la ventana
    root = tk.Tk()
    root.title("Prueba de BaseView")
    root.geometry("400x300")
    
    # Configurar estilo
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    
    # Crear un controlador simulado
    class MockController:
        pass
    
    # Crear y mostrar la vista
    view = TestView(root, MockController())
    view.pack(fill="both", expand=True)
    
    root.mainloop()
