# Graph Report - .  (2026-05-31)

## Corpus Check
- Corpus is ~10,618 words - fits in a single context window. You may not need a graph.

## Summary
- 422 nodes · 512 edges · 61 communities (23 shown, 38 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 104 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Database Model Layer|Database Model Layer]]
- [[_COMMUNITY_Controller Layer & Navigation|Controller Layer & Navigation]]
- [[_COMMUNITY_Playlist Management UI|Playlist Management UI]]
- [[_COMMUNITY_Playlist Model|Playlist Model]]
- [[_COMMUNITY_Download & Update Pipeline|Download & Update Pipeline]]
- [[_COMMUNITY_Development Guidelines|Development Guidelines]]
- [[_COMMUNITY_Base Views|Base Views]]
- [[_COMMUNITY_CLI Toolchain|CLI Toolchain]]
- [[_COMMUNITY_Update DB View|Update DB View]]
- [[_COMMUNITY_Spotify API Handler|Spotify API Handler]]
- [[_COMMUNITY_Manage Playlists Controller|Manage Playlists Controller]]
- [[_COMMUNITY_Agent Infrastructure Docs|Agent Infrastructure Docs]]
- [[_COMMUNITY_MVC Architecture Patterns|MVC Architecture Patterns]]
- [[_COMMUNITY_Base View Framework|Base View Framework]]
- [[_COMMUNITY_Base Controller Framework|Base Controller Framework]]
- [[_COMMUNITY_Database Utilities|Database Utilities]]
- [[_COMMUNITY_VSCode Settings|VSCode Settings]]
- [[_COMMUNITY_App Entrypoint|App Entrypoint]]
- [[_COMMUNITY_Azure Copilot Rules|Azure Copilot Rules]]
- [[_COMMUNITY_Playlist List|Playlist List]]
- [[_COMMUNITY_Song Title Builder|Song Title Builder]]
- [[_COMMUNITY_YouTube Search|YouTube Search]]
- [[_COMMUNITY_Audio Download|Audio Download]]
- [[_COMMUNITY_Playlist Table Schema|Playlist Table Schema]]
- [[_COMMUNITY_Add Playlist|Add Playlist]]
- [[_COMMUNITY_Retrieve Playlist By ID|Retrieve Playlist By ID]]
- [[_COMMUNITY_Retrieve Playlist By Name|Retrieve Playlist By Name]]
- [[_COMMUNITY_Delete Playlist|Delete Playlist]]
- [[_COMMUNITY_Update Playlist|Update Playlist]]
- [[_COMMUNITY_List All Playlists|List All Playlists]]
- [[_COMMUNITY_Update From JSON|Update From JSON]]
- [[_COMMUNITY_Generate Spotify URL|Generate Spotify URL]]
- [[_COMMUNITY_Songs Table Schema|Songs Table Schema]]
- [[_COMMUNITY_List Songs By Playlist|List Songs By Playlist]]
- [[_COMMUNITY_Add Song|Add Song]]
- [[_COMMUNITY_Retrieve Song By ID|Retrieve Song By ID]]
- [[_COMMUNITY_Delete Song|Delete Song]]
- [[_COMMUNITY_Update Song|Update Song]]
- [[_COMMUNITY_List All Songs|List All Songs]]
- [[_COMMUNITY_List Undownloaded Songs|List Undownloaded Songs]]
- [[_COMMUNITY_Check Song Field|Check Song Field]]
- [[_COMMUNITY_Mark Song Downloaded|Mark Song Downloaded]]
- [[_COMMUNITY_Mark Song Not Downloaded|Mark Song Not Downloaded]]
- [[_COMMUNITY_Test Song Setup|Test Song Setup]]
- [[_COMMUNITY_Test Spotify Setup|Test Spotify Setup]]
- [[_COMMUNITY_Singleton Reset|Singleton Reset]]
- [[_COMMUNITY_Type Hints Convention|Type Hints Convention]]
- [[_COMMUNITY_Error Handling Pattern|Error Handling Pattern]]
- [[_COMMUNITY_Database Operations Pattern|Database Operations Pattern]]
- [[_COMMUNITY_Code Formatting Rules|Code Formatting Rules]]
- [[_COMMUNITY_Git Practices|Git Practices]]
- [[_COMMUNITY_Adding New Tests Workflow|Adding New Tests Workflow]]
- [[_COMMUNITY_Glossary Vocabulary Convention|Glossary Vocabulary Convention]]
- [[_COMMUNITY_ADR Conflict Flagging|ADR Conflict Flagging]]

## God Nodes (most connected - your core abstractions)
1. `ManagePlaylistsView` - 25 edges
2. `UpdateDBController` - 21 edges
3. `get_db_connection()` - 21 edges
4. `ManagePlaylistsController` - 19 edges
5. `UpdateDBView` - 17 edges
6. `Song` - 16 edges
7. `Playlist` - 15 edges
8. `SpotifyAPIHandler` - 13 edges
9. `MainController` - 13 edges
10. `BaseView` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Top Hits Analyser` --references--> `GitHub Repository (xG3R4RD0x/top-hits-analyser)`  [INFERRED]
  AGENTS.md → README.md
- `migrate_excel_to_db()` --calls--> `insert_song()`  [INFERRED]
  migrate_excel_to_db.py → db_utils.py
- `SpotifyPlaylistAnalyzer` --uses--> `YouTubeAudioDownloader`  [INFERRED]
  hit-analyser.py → get_music.py
- `main()` --calls--> `YouTubeAudioDownloader`  [INFERRED]
  hit-analyser.py → get_music.py
- `SpotifyPlaylistAnalyzer` --uses--> `YouTubeSearcher`  [INFERRED]
  hit-analyser.py → search_songs.py

## Hyperedges (group relationships)
- **Project Architecture** — AGENTS_TopHitsAnalyser, AGENTS_MVCArchitecture, AGENTS_ControllerLayer, AGENTS_ModelLayer, AGENTS_ViewLayer, AGENTS_TestLayer [EXTRACTED 1.00]
- **CLI Toolchain** — README_hitAnalyser, README_searchSongs, README_getSongs, README_playlistsJson, README_xlsxFile [EXTRACTED 1.00]
- **External Dependencies** — REQS_ffmpeg, REQS_pandas, REQS_pythonDotenv, REQS_spotipy, REQS_ytDlp [EXTRACTED 1.00]
- **Triage Label System** — TRIAGE_TriageLabels, TRIAGE_NeedsTriage, TRIAGE_NeedsInfo, TRIAGE_ReadyForAgent, TRIAGE_ReadyForHuman, TRIAGE_Wontfix [EXTRACTED 1.00]
- **Agent Skills Infrastructure** — AGENTS_AgentSkills, ISSUETRACKER_GitHubIssues, TRIAGE_TriageLabels, DOMAIN_DomainDocs [EXTRACTED 1.00]

## Communities (61 total, 38 thin omitted)

### Community 0 - "Database Model Layer"
Cohesion: 0.07
Nodes (27): get_db_connection(), initialize_db(), Get the database connection., Initialize the database connection., Make the object iterable by returning an iterator over its attributes., Song, add_song(), check_field_value() (+19 more)

### Community 1 - "Controller Layer & Navigation"
Cohesion: 0.07
Nodes (18): BaseController, MainController, Initialize all frames/views of the application and add them to the view manager., Navigate to a specific view by name.         Args:             view_name: The, DatabaseController, Handle navigation events from the view, Update the data displayed in the database view., Specific controller for the database view (+10 more)

### Community 2 - "Playlist Management UI"
Cohesion: 0.07
Nodes (15): ManagePlaylistsView, View to display playlists, Load playlists into the treeview, Muestra el formulario para agregar playlist (modo agregar), Oculta los campos y botones guardar/cancelar, muestra solo el botón volver, Muestra el formulario para editar playlist (modo edición), Handler para el botón de agregar playlist, Handler for edit playlist action (+7 more)

### Community 3 - "Playlist Model"
Cohesion: 0.10
Nodes (17): Playlist, Convert the playlist object to a tuple for database operations., add_playlist(), _create_table(), delete_playlist(), generate_playlist_url_from_id(), get_playlist(), get_playlist_by_name() (+9 more)

### Community 4 - "Download & Update Pipeline"
Cohesion: 0.09
Nodes (15): Specific controller for the database update view, Download songs from the database using multithreading without blocking the GUI., Register specific events for the database update view, Cancel the update operation in progress., Itera por las canciones y comprueba si están descargadas usando Downloader.check, Handle navigation events from the view, Start the database update process, Fetch songs from a specific playlist and return them as a list of Song objects. (+7 more)

### Community 5 - "Development Guidelines"
Cohesion: 0.11
Nodes (23): CLI Version (hit-analyser.py), Code Style Guidelines, Project Dependencies, FFmpeg Requirement, GUI Version (run_app.py), Testing Guidelines, Top Hits Analyser, unittest Framework (+15 more)

### Community 6 - "Base Views"
Cohesion: 0.09
Nodes (12): BaseView, DatabaseView, Crear un Treeview para mostrar los datos de las canciones, Vista para mostrar y gestionar la base de datos, Actualizar los datos en la vista, Volver al menú principal, Añadir datos al tree view, MainMenuView (+4 more)

### Community 7 - "CLI Toolchain"
Cohesion: 0.15
Nodes (6): main(), read_songs_from_file(), YouTubeAudioDownloader, main(), SpotifyPlaylistAnalyzer, YouTubeSearcher

### Community 8 - "Update DB View"
Cohesion: 0.13
Nodes (10): MockMainController, Update progress bar and optionally the percentage text          Args:, Add a message to the log area          Args:             message: Message to, Download songs from the database, Check if songs are downloaded, Fetch songs URLs from the database, Start the update operation, Cancel the ongoing operation (+2 more)

### Community 9 - "Spotify API Handler"
Cohesion: 0.12
Nodes (8): Extract playlist ID from a Spotify URL., Fetch tracks from a playlist and return them as Song objects., Extract playlist ID and name from a Spotify URL.                  fields for p, SpotifyAPIHandler, Test the get_tracks_from_playlist function., Test the get_playlist_metadata_from_URL function., setUpClass(), TestSpotifyAPIHandler

### Community 10 - "Manage Playlists Controller"
Cohesion: 0.13
Nodes (8): ManagePlaylistsController, Specific controller for the database update view, Register specific events for the database update view, Handle navigation events from the view, Cancel the update operation in progress., Save a new playlist to the database., Update an existing playlist in the database., delete a playlist from the database.

### Community 11 - "Agent Infrastructure Docs"
Cohesion: 0.13
Nodes (17): Agent Skills, ADR Directory (docs/adr/), CONTEXT-MAP.md, CONTEXT.md, Domain Documentation Structure, Multi-Context Repository Pattern, Single-Context Repository Pattern, Add QA Issues to Global Board Workflow (+9 more)

### Community 12 - "MVC Architecture Patterns"
Cohesion: 0.19
Nodes (15): Adding a New Feature Workflow, Controller Layer (app/controller/), Database Schema Changes Workflow, File Organization (app/ structure), Import Guidelines, MVC Architecture, MainController, Model Layer (app/model/) (+7 more)

### Community 13 - "Base View Framework"
Cohesion: 0.15
Nodes (6): BaseView, Override __new__ to implement the singleton pattern, Method that each subclass must implement to set up its UI., Register a handler for a specific event., Trigger an event with the provided arguments., Base class for all views/frames of the application.

### Community 14 - "Base Controller Framework"
Cohesion: 0.17
Nodes (7): BaseController, Set the view that this controller manages and register events.          Args:, Register events for the specific view.         Each controller subclass should, This method is called to update the view on show         Just in case it needs, Base controller that defines the common interface for all controllers, Navigate to a specific view.          Args:             view_name: Name of th, Initialize the base controller.          Args:             main_controller: R

### Community 16 - "VSCode Settings"
Cohesion: 0.50
Nodes (3): python.testing.pytestEnabled, python.testing.unittestArgs, python.testing.unittestEnabled

## Knowledge Gaps
- **13 isolated node(s):** `playlists`, `python.testing.unittestArgs`, `python.testing.pytestEnabled`, `python.testing.unittestEnabled`, `GUI Version (run_app.py)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ManagePlaylistsView` connect `Playlist Management UI` to `Controller Layer & Navigation`, `Playlist Model`, `Base Views`, `Manage Playlists Controller`, `Base View Framework`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `UpdateDBController` connect `Download & Update Pipeline` to `Database Model Layer`, `Controller Layer & Navigation`, `Playlist Model`, `Update DB View`, `Base Controller Framework`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `MainController` connect `Controller Layer & Navigation` to `Playlist Management UI`, `Download & Update Pipeline`, `Base Views`, `Update DB View`, `Manage Playlists Controller`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ManagePlaylistsView` (e.g. with `MainController` and `ManagePlaylistsController`) actually correct?**
  _`ManagePlaylistsView` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `UpdateDBController` (e.g. with `MainController` and `BaseController`) actually correct?**
  _`UpdateDBController` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `get_db_connection()` (e.g. with `_create_table()` and `add_playlist()`) actually correct?**
  _`get_db_connection()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ManagePlaylistsController` (e.g. with `MainController` and `BaseController`) actually correct?**
  _`ManagePlaylistsController` has 7 INFERRED edges - model-reasoned connections that need verification._