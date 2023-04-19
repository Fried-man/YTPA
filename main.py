"""
main.py: Analyzes the genres of tracks in a YouTube Music playlist using the Spotify API.

This script takes a YouTube Music playlist URL as input and prints the percentage of each genre
in the playlist based on the Spotify API's genre information for the corresponding tracks.

Modules:
    - youtube: Functions for interacting with the YouTube API.
    - spotify: Functions for interacting with the Spotify API.

Functions:
    main(): Main function that drives the analysis and output.
"""

from youtube import *
from spotify import *

def main():
    """
    Main function that drives the analysis and output.
    """

    # Takes a YouTube Music playlist URL as user input.
    playlist_url = input("Enter a YouTube Music playlist URL: ")

    # Extracts the playlist ID from the URL.
    playlist_id = get_playlist_id(playlist_url)

    if not playlist_id:
        print("Invalid URL")
        return

    # Fetches video IDs from the playlist using the YouTube API.
    video_ids = get_video_ids(YOUTUBE_API_KEY, playlist_id)
    if len(video_ids) == 0:
        return

    # Fetches video titles for the video IDs using the YouTube API.
    video_titles = get_video_titles(YOUTUBE_API_KEY, video_ids)

    genre_count = defaultdict(int)
    total_genres = 0

    # Obtains a Spotify API access token using the client ID and client secret.
    spotify_access_token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    if spotify_access_token is None:
        return

    # Fetches genres for each track using the Spotify API.
    for title in video_titles:
        genres = get_genres_for_track(spotify_access_token, title)
        for genre in genres:
            genre_count[genre] += 1
            total_genres += 1

    # Counts the occurrences of each genre and calculates their percentages.
    ranked_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

    # Prints the ranked list of genre percentages.
    print("Genre percentages for the playlist:")
    for genre, count in ranked_genres:
        percentage = (count / total_genres) * 100
        print(f"{genre}: {percentage:.2f}%")

if __name__ == "__main__":
    main()
