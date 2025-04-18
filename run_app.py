import tkinter as tk
import sqlite3
import atexit
from app.controller.controller import MainController

# Configuración de la base de datos global
DB_CONNECTION = sqlite3.connect("tracks.db", check_same_thread=False)


def close_connection():
    """Cerrar la conexión a la base de datos al salir."""
    if DB_CONNECTION:
        DB_CONNECTION.close()
        print("Conexión a la base de datos cerrada correctamente.")


# Registrar la función para cerrar la conexión al salir
atexit.register(close_connection)


def main():
    """
    Punto de entrada principal para la aplicación.
    Inicializa la interfaz gráfica y lanza el controlador principal.
    """
    # Crear la ventana principal
    root = tk.Tk()

    # Inicializar el controlador principal (que a su vez inicializa la vista)
    controller = MainController(root)

    # Mostrar la vista inicial (menú principal)
    controller.navigate_to("main_menu")

    # Iniciar el bucle principal de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()
