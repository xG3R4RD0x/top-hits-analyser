# Spotify to MP3 Downloader

This program allows you to download songs from Spotify playlists in MP3 format using their corresponding YouTube videos.

## Description

The program fetches songs from specified Spotify playlists and downloads their audio tracks from YouTube. It saves these tracks in MP3 format with proper naming conventions.

## Features

- Fetch Spotify playlists and retrieve song details.
- Search YouTube for the corresponding videos of the songs.
- Download audio tracks from YouTube and convert them to MP3.
- Automatically handle duplicate checks and re-downloads only if necessary.

## Requirements

- [FFmpeg](https://ffmpeg.org/download.html) must be installed and added to your system's PATH.
- Python 3.x

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/xG3R4RD0x/top-hits-analyser.git
   cd top-hits-analyser
   ```

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up Spotify API credentials:
   - Create a Spotify app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Replace the credentials in `hit_analyser.py` with your app's client ID and client secret.

## Configuration

- To add playlists for downloading, edit the `playlists.json` file and add the playlist name and ID.

## Usage

1. Run the `hit_analyser.py` script and select an option:

   ```sh
   python hit_analyser.py
   ```

   - Option 1: Update the song list in the `.xlsx` file.
   - Option 2: Download the songs from the `.xlsx` file.
   - Option 3: Update the song list and download the songs.

### Detailed Script Functionality

- `hit_analyser.py`: Main script for interacting with the user. It provides options to update song lists and download songs.
- `search_songs.py`: Searches for each song on YouTube and copies the video URL to the song's information.
- `get_songs.py`: Downloads the audio from the URL of each song, renames it, and saves it in the directory specified in `hit_analyser.py`.

## Example

To add a playlist to `playlists.json`:

```json
{
  "playlists": [
    {
      "name": "Mansion Reggaeton",
      "id": "37i9dQZF1DXc4CrXglGoXU"
    },
    {
      "name": "Top Hits",
      "id": "37i9dQZF1DXcBWIGoYBM5M"
    }
  ]
}
```
