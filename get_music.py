import os
from yt_dlp import YoutubeDL
import ffmpeg
import pandas as pd


class YouTubeAudioDownloader:
    def __init__(self, tracks):
        self.tracks = tracks  # Lista de diccionarios con información de las canciones

    def download_songs(self, output_path="music/hits"):
        # Crear el directorio si no existe
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",  # Descargar el mejor audio disponible
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "noplaylist": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            for track in self.tracks:
                url = track.get(
                    "YouTube URL"
                )  # Obtén la URL directamente del diccionario
                try:
                    # Obtener información del video sin descargar
                    info = ydl.extract_info(url, download=False)
                    video_title = info["title"]
                    print(f"Verificando si el audio de: {video_title} ya existe")

                    # Preparar nombres de archivo
                    input_file = ydl.prepare_filename(info)
                    if input_file.endswith(".webm"):
                        output_file = input_file.replace(".webm", ".mp3")
                    else:
                        output_file = input_file + ".mp3"

                    # Verificar si el archivo ya existe
                    if not os.path.isfile(output_file):
                        print(f"Descargando audio de: {video_title}")
                        ydl.download([url])
                        self.convert_to_mp3(input_file, output_file)
                        print(f"Audio descargado y convertido a MP3: {output_file}")
                    else:
                        print(f"Archivo ya existe: {output_file}")
                except Exception as e:
                    print(f"Error al descargar {url}: {e}")

    def convert_to_mp3(self, input_file, output_file):
        try:
            # Usa ffmpeg-python para convertir el archivo de audio con alta calidad
            ffmpeg.input(input_file).output(
                output_file, format="mp3", audio_bitrate="320k", q="0"
            ).run()
            os.remove(input_file)  # Elimina el archivo original si es necesario
        except Exception as e:
            print(f"Error al convertir {input_file} a MP3: {e}")

    @staticmethod
    def read_songs_from_file(file_path):
        try:
            # Leer el archivo Excel
            df = pd.read_excel(file_path)

            # Verificar si el archivo contiene las columnas esperadas
            expected_columns = {
                "playlist_name",
                "name",
                "artist",
                "album",
                "release_date",
                "YouTube URL",
            }
            if not expected_columns.issubset(df.columns):
                raise ValueError("El archivo Excel no contiene las columnas esperadas.")

            # Convertir el DataFrame en una lista de diccionarios
            songs_list = df.to_dict(orient="records")
            return songs_list

        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            return []


def main():
    # tracks = YouTubeAudioDownloader.read_songs_from_file("./playlist_tracks.xlsx")

    # downloader = YouTubeAudioDownloader(tracks)
    # downloader.download_songs()
    tracks = [
        {
            "playlist_name": "Mansion Reggaeton",
            "name": "Cuatro Babys",
            "artist": "Maluma, Trap Capos, Noriel, Bryant Myers, Juhn",
            "album": "Cuatro Babys",
            "release_date": "2016-12-09",
            "YouTube URL": "https://www.youtube.com/watch?v=OXq-JP8w5H4",
        },
        {
            "playlist_name": "Reggaeton 2024",
            "name": "Frida Calo",
            "artist": "test",
            "album": "test",
            "release_date": "2020-08-21",
            "YouTube URL": "https://www.youtube.com/watch?v=76uZChJs9XA",
        },
        # Agrega más canciones aquí
    ]

    downloader = YouTubeAudioDownloader(tracks)
    downloader.download_songs()


if __name__ == "__main__":
    main()
