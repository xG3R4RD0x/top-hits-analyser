from yt_dlp import YoutubeDL
import re


class YouTubeSearcher:
    def __init__(self):
        self.ydl_opts = {
            "format": "best",
            "quiet": True,
            "noplaylist": True,
            "extract_flat": True,  # Esto evita la descarga completa y solo extrae la información
            "force_generic_extractor": True,  # Asegura que se utilice un extractor genérico para la búsqueda
        }

    def search_youtube(self, query):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                # Busca en YouTube
                result = ydl.extract_info(f"ytsearch:{query}", download=False)
                if "entries" in result and len(result["entries"]) > 0:
                    # Obtén la URL del video completo
                    return result["entries"][0]["url"]
            except Exception as e:
                print(f"Error al buscar en YouTube: {e}")
        return None

    def add_youtube_urls_to_tracks(tracks):
        searcher = YouTubeSearcher()

        for track in tracks:
            query = f"{track['name']} {track['artist']}"
            print(f"Buscando: {query}")
            youtube_url = searcher.search_youtube(query)
            track["YouTube URL"] = youtube_url

        return tracks


# def main():
#     # Lista de canciones como diccionarios
#     tracks = [
#         {
#             "playlist_name": "Mansion Reggaeton",
#             "name": "Cuatro Babys",
#             "artist": "Maluma, Trap Capos, Noriel, Bryant Myers, Juhn",
#             "album": "Cuatro Babys",
#             "release_date": "2016-12-09",
#         },
#         {
#             "playlist_name": "Top Reggaeton Hits",
#             "name": "Hawái",
#             "artist": "Maluma",
#             "album": "Papi Juancho",
#             "release_date": "2020-08-21",
#         },
#         # Agrega más canciones aquí
#     ]

#     updated_tracks = add_youtube_urls_to_tracks(tracks)
#     save_tracks_to_excel(updated_tracks)


# if __name__ == "__main__":
#     main()
