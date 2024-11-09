import os
from yt_dlp import YoutubeDL
import ffmpeg
import pandas as pd
import glob


class YouTubeAudioDownloader:
    def __init__(self, tracks):
        self.tracks = tracks  # Lista de diccionarios con información de las canciones

    def download_songs(self, output_path="music/hits"):
        # Crear el directorio si no existe
        os.makedirs(output_path, exist_ok=True)

        # Verificar y crear una lista de tracks a descargar
        tracks_to_download = self.get_tracks_to_download(output_path)

        with YoutubeDL() as ydl:
            for track in tracks_to_download:
                url = track.get(
                    "YouTube URL"
                )  # Obtén la URL directamente del diccionario
                video_title = f"{track['artist']} - {track['name']}"
                ydl_opts = {
                    "format": "bestaudio/best",  # Descargar el mejor audio disponible
                    "outtmpl": os.path.join(output_path, f"{video_title}.%(ext)s"),
                    "noplaylist": True,
                    "postprocessors": [
                        {  # Postprocesador para convertir a mp3
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
                try:
                    with YoutubeDL(ydl_opts) as ydl_with_opts:
                        # Obtener información del video sin descargar
                        info = ydl_with_opts.extract_info(url, download=False)
                        print(f"Verificando si el audio de: {video_title} ya existe")

                        # Comprobar si ya existe un archivo con el nombre del video en cualquier formato
                        existing_files = glob.glob(
                            os.path.join(output_path, f"*{video_title}*")
                        )

                        if existing_files:
                            print(
                                f"Archivos existentes encontrados para {video_title}: {existing_files}"
                            )
                            for file in existing_files:
                                if not file.endswith(".mp3"):
                                    print(
                                        f"Archivo de formato no MP3 encontrado: {file}, convirtiendo a MP3"
                                    )
                                    self.convert_to_mp3(
                                        file,
                                        file.replace(os.path.splitext(file)[1], ".mp3"),
                                    )
                            continue  # Pasar al siguiente track

                        # Descargar el archivo si no existe en ningún formato
                        print(f"Descargando audio de: {video_title}")
                        ydl_with_opts.download([url])

                except Exception as e:
                    print(f"Error al descargar {url}: {e}")

    def get_tracks_to_download(self, output_path):
        existing_files = glob.glob(os.path.join(output_path, "*.mp3"))
        existing_titles = [
            os.path.splitext(os.path.basename(f))[0] for f in existing_files
        ]
        tracks_to_download = []

        for track in self.tracks:
            track_title = f"{track['artist']} - {track['name']}"
            if track_title not in existing_titles:
                tracks_to_download.append(track)
            else:
                print(f"El archivo ya existe: {track_title}")

        print("existen: " + len(tracks_to_download) + "tracks nuevos")

        return tracks_to_download

    def convert_to_mp3(self, input_file, output_file):
        try:
            # Usa ffmpeg-python para convertir el archivo de audio con alta calidad
            ffmpeg.input(input_file).output(output_file, format="mp3").run()
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
    tracks = YouTubeAudioDownloader.read_songs_from_file("./playlist_tracks.xlsx")

    downloader = YouTubeAudioDownloader(tracks)
    downloader.download_songs()
    # tracks = downloader.get_tracks_to_download("music/hits")


if __name__ == "__main__":
    main()
