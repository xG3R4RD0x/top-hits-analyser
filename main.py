import sys
import os

# Aseguramos que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tkinter import Tk
from app.controller import MainController

def main():
    """
    Punto de entrada principal para la aplicación.
    Inicializa la interfaz gráfica y lanza el controlador principal.
    """
    root = Tk()
    controller = MainController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
