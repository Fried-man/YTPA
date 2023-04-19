"""
spotify.py: Functions for interacting with the Spotify API.

This module provides functions to obtain an access token and fetch genres for a given track title.

Functions:
    - get_spotify_access_token(client_id, client_secret): Obtains a Spotify API access token.
    - get_genres_for_track(spotify_access_token, track_title): Fetches genres for a given track title using the Spotify API.
"""

import base64
import requests
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def get_spotify_access_token(client_id, client_secret):
    """
    Obtains a Spotify API access token using the provided client ID and client secret.

    Args:
        client_id (str): The Spotify client ID.
        client_secret (str): The Spotify client secret.

    Returns:
        str: The Spotify access token if successful, otherwise None.
    """

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    # Create the Authorization header for the request
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    }
    response = requests.post(auth_url, data=auth_data, headers=auth_header)

    # Handle errors in the API response
    if response.status_code != 200:
        response_json = response.json()
        if response.status_code == 400 and response_json.get('error') == 'invalid_client':
            print("Invalid client. Please check your client_id and client_secret.")
        else:
            print(f"Error obtaining Spotify access token: {response.status_code} - {response.text}")
        return None

    return response.json()['access_token']

def get_genres_for_track(spotify_access_token, track_title):
    """
    Fetches genres for a given track title using the Spotify API.

    Args:
        spotify_access_token (str): The Spotify API access token.
        track_title (str): The title of the track to search for.

    Returns:
        list: A list of genres associated with the track's primary artist if found, otherwise an empty list.
    """

    search_url = 'https://api.spotify.com/v1/search'
    search_params = {
        'q': track_title,
        'type': 'track',
        'limit': 1
    }
    search_header = {
        'Authorization': f'Bearer {spotify_access_token}'
    }
    response = requests.get(search_url, params=search_params, headers=search_header)

    # Handle errors in the API response
    if response.status_code != 200:
        print(f"Error searching for track: {response.status_code} - {response.text}")
        return []

    search_result = response.json()
    if search_result.get('tracks', {}).get('items'):
        track = search_result['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
    else:
        print("Track not found on Spotify")
        return []

    # Fetch artist details using the artist ID
    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    response = requests.get(artist_url, headers=search_header)
    
    # Handle errors in the API response
    if response.status_code != 200:
        print(f"Error fetching artist details: {response.status_code} - {response.text}")
        return []

    artist = response.json()
    return artist['genres']
