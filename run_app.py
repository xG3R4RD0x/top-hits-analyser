from tkinter import Tk
from app.model.db_config import initialize_db

# Initialize the DB connection first
DB_CONNECTION = initialize_db("tracks.db")

# Now import the controller
from app.controller.controller import MainController

import atexit


def close_connection():
    """Cerrar la conexión a la base de datos al salir."""
    if DB_CONNECTION:
        DB_CONNECTION.close()
        print("Conexión a la base de datos cerrada correctamente.")


# Registrar la función para cerrar la conexión al salir
atexit.register(close_connection)

if __name__ == "__main__":
    root = Tk()
    app = MainController(root)
    root.mainloop()
