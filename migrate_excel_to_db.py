import pandas as pd
from db_utils import insert_song

# Define la ruta a tu archivo Excel
EXCEL_PATH = "./playlist_tracks.xlsx"


def migrate_excel_to_db(excel_path):
    # Leer el archivo Excel
    df = pd.read_excel(excel_path)

    # Verificar que las columnas necesarias están presentes
    required_columns = [
        "playlist_name",
        "name",
        "artist",
        "album",
        "release_date",
        "YouTube URL",
    ]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"El archivo de Excel debe contener la columna '{column}'")

    # Iterar sobre las filas del DataFrame e insertar cada canción en la base de datos
    for _, row in df.iterrows():
        song = {
            "playlist_name": row["playlist_name"],
            "name": row["name"],
            "artist": row["artist"],
            "album": row["album"],
            "release_date": row["release_date"],
            "youtube_url": row["YouTube URL"],
        }
        insert_song(song)


# Ejecutar la migración
migrate_excel_to_db(EXCEL_PATH)
