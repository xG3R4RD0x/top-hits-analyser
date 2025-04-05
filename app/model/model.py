import pandas as pd
import os
import sys
from pathlib import Path

# Aseguramos que podamos importar módulos del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from search_songs import YouTubeSearcher
from get_music import YouTubeAudioDownloader
import db_utils

class DatabaseModel:
    """Modelo para gestionar la base de datos de canciones y realizar operaciones de descarga."""
    
    def __init__(self):
        self.excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                     "playlist_tracks.xlsx")
        
    def update_database(self):
        """Actualiza la base de datos de canciones desde Spotify."""
        # Aquí implementarías la lógica para actualizar la base de datos
        # Usando las clases existentes en hit-analyser.py
        pass
        
    def download_songs(self):
        """Descarga las canciones de la base de datos."""
        try:
            # Lee la lista de canciones del archivo Excel
            tracks = YouTubeAudioDownloader.read_songs_from_file(self.excel_path)
            # Descarga las canciones
            downloader = YouTubeAudioDownloader(tracks)
            downloader.download_songs()
            return True
        except Exception as e:
            print(f"Error al descargar canciones: {e}")
            return False
            
    def check_database_status(self):
        """Comprueba el estado de la base de datos."""
        try:
            # Verificar si existe el archivo Excel
            if os.path.exists(self.excel_path):
                df = pd.read_excel(self.excel_path)
                return f"Base de datos OK. {len(df)} canciones encontradas."
            else:
                return "El archivo de base de datos no existe."
        except Exception as e:
            return f"Error al verificar la base de datos: {e}"
            
    def get_database_content(self):
        """Obtiene el contenido de la base de datos."""
        try:
            if os.path.exists(self.excel_path):
                return pd.read_excel(self.excel_path)
            else:
                return "No hay datos disponibles."
        except Exception as e:
            return f"Error al leer la base de datos: {e}"
