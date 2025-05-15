from app.controller.base_controller import BaseController
from app.model.playlists import Playlists
from app.model.songs import Songs
from app.model.downloader import Downloader
import threading
from concurrent.futures import ThreadPoolExecutor
from app.view.manage_playlists_view import ManagePlaylistsView


class ManagePlaylistsController(BaseController):
    """Specific controller for the database update view"""

    def __init__(self, main_controller):
        super().__init__(main_controller)
        self.stop_update = False

    def register_events(self):
        """Register specific events for the database update view"""
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler(
            "cancel_update_operation", self.cancel_update_operation
        )
        self.view.register_event_handler("extract_data_from_url", self.extract_data_from_url)
        self.view.register_event_handler("save_new_playlist", self.save_new_playlist)
        self.view.register_event_handler("update_playlist", self.update_playlist)
        self.view.register_event_handler("delete_playlist", self.delete_playlist)
    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    # def add_new_playlists(self):
    # """tengo que prgramar una forma de agregar nuevas playlists"""
    # la idea es que se vea y funcione como el menu de agregar global variables de windows
    # para eso se necesita una tabla con los nombres de las playlists y un boton para agregar una nueva playlist
    # y otro para eliminar una playlist existente
    # debe haber uno para editar el nombre de la playlist
    # además se debe crear una funcion para extraer el ID y el nombre directo de la URL de la playlist

    def update_view(self):
        playlists = Playlists.list_playlists()
        self.view.load_playlists(playlists)
        
        print("Manage playlist controller updated")
        
        

    def cancel_update_operation(self):
        """Cancel the update operation in progress."""
        print("UpdateDBController: Cancelling update operation...")
        self.view.cancelled = True
        self.stop_update = True
        self.view.complete_operation(False)
        
    def extract_data_from_url(self, url):
        id, name = self.sp.get_playlist_metadata_from_url(url)
        if id is None or name is None:
            id, name = "", ""
        print(f"Extracted data from URL: {id}, {name}")
        self.view.on_url_data_extracted(id, name)
        
    def save_new_playlist(self, id, name):
        """Save a new playlist to the database."""
        print(f"Saving new playlist: {id}, {name}")
        Playlists.add_playlist(id= id, name = name)
        self.update_view()
        
    def update_playlist(self,playlist, playlist_id, name):
        """Update an existing playlist in the database."""
        print(f"Updating playlist: {id}, {name}")
        Playlists.update_playlist(playlist= playlist,playlist_id= playlist_id, name = name)
        self.update_view()  
        
    def delete_playlist(self, playlist_id):
        """delete a playlist from the database."""
        print(f"Deleting playlist: {playlist_id}")
        Playlists.delete_playlist(playlist_id)
        self.update_view()
        
