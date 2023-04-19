# Youtube Music Playlist Analyser

Youtube Music Playlist Analyser is a tool that analyses the genres of tracks in a YouTube Music playlist using data from the Spotify API.

## Features

- Extracts video IDs and titles from a YouTube Music playlist URL
- Fetches genres for each track using the Spotify API
- Calculates and displays the percentage of each genre in the playlist

## Installation

1. Clone the repository: ```git clone https://github.com/Fried-man/YTPA```
2. Change to the project directory: ```cd YTPA```
3. Install the required dependencies

## Configuration

1. Create a `config.py` file in the project directory.
2. Set up a YouTube API key and Spotify API credentials (client ID and client secret). You can obtain them from the [Google Developer Console](https://console.developers.google.com/) and the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications), respectively.
3. Add the API keys and credentials to the `config.py` file:
```
YOUTUBE_API_KEY = "your_youtube_api_key"
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
```

## Usage
1. Run the main.py script: ```python main.py```
2. Enter a YouTube Music playlist URL when prompted
3. The script will analyze the genres of the tracks in the playlist and print the ranked list of genre percentages.
