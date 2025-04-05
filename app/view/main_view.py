import tkinter as tk

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Hits Downloader")
        self.root.geometry("400x300")

        # Encabezado
        self.label = tk.Label(self.root, text="Hits Downloader", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Botones
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=10)

        self.update_and_download_button = tk.Button(
            self.buttons_frame, text="Actualizar base de datos y descargar canciones"
        )
        self.update_and_download_button.pack(fill="x", pady=5)

        self.check_database_button = tk.Button(
            self.buttons_frame, text="Revisar base de datos actual"
        )
        self.check_database_button.pack(fill="x", pady=5)

        self.update_database_button = tk.Button(
            self.buttons_frame, text="Actualizar base de datos"
        )
        self.update_database_button.pack(fill="x", pady=5)

        self.download_with_database_button = tk.Button(
            self.buttons_frame, text="Descargar canciones con base de datos actual"
        )
        self.download_with_database_button.pack(fill="x", pady=5)

        self.view_database_button = tk.Button(
            self.buttons_frame, text="Ver base de datos"
        )
        self.view_database_button.pack(fill="x", pady=5)

    def set_button_commands(self, commands):
        """
        Permite configurar los comandos de los botones desde el controlador.
        :param commands: Diccionario con los comandos para cada botón.
        """
        self.update_and_download_button.config(command=commands.get("update_and_download"))
        self.check_database_button.config(command=commands.get("check_database"))
        self.update_database_button.config(command=commands.get("update_database"))
        self.download_with_database_button.config(command=commands.get("download_with_database"))
        self.view_database_button.config(command=commands.get("view_database"))

if __name__ == "__main__":
    root = tk.Tk()
    main_view = MainView(root)
    root.mainloop()
