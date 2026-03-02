# AGENTS.md - Development Guidelines for Top Hits Analyser

## Project Overview

This is a Python-based Tkinter GUI application that downloads Spotify playlist songs from YouTube as MP3 files. The project follows an MVC (Model-View-Controller) architecture.

## Build/Lint/Test Commands

### Running the Application

```bash
# Run the CLI version
python hit-analyser.py

# Run the GUI version
python run_app.py
```

### Running Tests

This project uses Python's built-in `unittest` framework.

```bash
# Run all tests (from project root)
python -m unittest discover -s ./app -p "*_test.py" -v

# Run a single test file
python -m unittest app.test.songs_test -v

# Run a specific test class
python -m unittest app.test.songs_test.TestSongs -v

# Run a specific test method
python -m unittest app.test.songs_test.TestSongs.test_list_songs_from_playlist -v

# Using VSCode Test Explorer (recommended for development)
# Tests are automatically discovered and can be run via the Testing sidebar
```

### Dependencies

```bash
# Install dependencies
pip install -r requirements.txt

# Requirements: ffmpeg, pandas, python-dotenv, spotipy, yt_dlp
```

**Note**: FFmpeg must be installed and in your system's PATH for audio conversion.

## Code Style Guidelines

### Naming Conventions

- **Classes**: PascalCase (e.g., `Song`, `Songs`, `MainController`)
- **Functions/Variables**: snake_case (e.g., `get_db_connection`, `playlist_name`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DB_CONNECTION`)
- **Test files**: `*_test.py` suffix (e.g., `songs_test.py`)
- **Test classes**: `Test` prefix (e.g., `TestSongs`)
- **Test methods**: `test_` prefix (e.g., `test_list_songs_from_playlist`)

### File Organization

```
app/
├── controller/    # Business logic (MVC Controllers)
├── model/         # Data models and database operations
├── view/          # Tkinter views/UI components
└── test/          # Unit tests
```

### Import Guidelines

- Standard library imports first
- Third-party imports second
- Local application imports third
- Sort imports alphabetically within each group
- Use absolute imports (e.g., `from app.model.song import Song`)

Example:
```python
import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from app.model.song import Song
from app.model.songs import Songs
```

### Type Hints

Add type hints where beneficial, especially for function parameters and return types:

```python
def get_db_connection() -> sqlite3.Connection:
    ...

def list_songs_from_playlist(playlist_id: int) -> list[Song]:
    ...
```

### Error Handling

- Use try/except blocks for operations that may fail (database, network, file I/O)
- Catch specific exceptions rather than using bare `except:`
- Log errors appropriately or display user-friendly messages in the UI
- Example pattern:

```python
try:
    songs = Songs.list_songs_from_playlist(playlist_id)
except sqlite3.Error as e:
    print(f"Database error: {e}")
    # Handle gracefully
```

### Database Operations

- Use parameterized queries to prevent SQL injection
- Always close database connections or use context managers
- Follow the existing pattern in `db_config.py` for connection management

### Testing Guidelines

- Write unit tests for all model and controller functions
- Use `unittest.mock.patch` to mock external dependencies (database, APIs)
- Follow the existing test structure in `app/test/`
- Tests should be self-contained and not depend on external state

Example test pattern:
```python
@patch("app.model.songs.get_db_connection")
def test_list_songs_from_playlist(self, mock_get_db_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [...]

    songs = Songs.list_songs_from_playlist(1)
    self.assertEqual(len(songs), 2)
```

### Code Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 120 characters (soft limit)
- Use blank lines to separate logical sections within functions
- Add docstrings to classes and public functions

### Git Practices

- Create feature branches for new functionality
- Write meaningful commit messages
- Do not commit secrets (API keys, credentials) - use `.env` files
- The `.env` file is in `.gitignore`

## External AI Assistant Rules

### Copilot Instructions (from .github/copilot-instructions.md)

- **Azure Rule**: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke the `azure_development-get_best_practices` tool if available.

(Note: This project is not Azure-focused, so this rule rarely applies)

## Common Development Tasks

### Adding a New Feature

1. Create model class in `app/model/`
2. Create view class in `app/view/`
3. Create controller class in `app/controller/`
4. Add tests in `app/test/`
5. Register the new view/controller in `MainController`

### Database Schema Changes

1. Modify `db_utils.py` or create migration scripts
2. Update `init_db.py` if needed
3. Test with a fresh database

### Adding New Tests

1. Create `app/test/your_feature_test.py`
2. Use `unittest.TestCase`
3. Mock external dependencies
4. Run tests to verify
