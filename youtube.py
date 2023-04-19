"""
youtube.py: Functions for interacting with the YouTube API.

This module provides functions to extract video IDs and titles from a YouTube Music playlist.

Functions:
    - get_playlist_id(url): Extracts the playlist ID from a YouTube Music playlist URL.
    - get_video_ids(api_key, playlist_id): Fetches video IDs from a YouTube playlist using the YouTube API.
    - get_video_titles(api_key, video_ids): Fetches video titles for the given video IDs using the YouTube API.
"""

import requests
import re
from collections import defaultdict
from config import YOUTUBE_API_KEY

def get_playlist_id(url):
    """
    Extracts the playlist ID from a YouTube Music playlist URL.

    Args:
        url (str): The YouTube Music playlist URL.

    Returns:
        str: The playlist ID if found, otherwise None.
    """
    # Define the regular expression pattern for extracting the playlist ID
    pattern = r'(?:list=)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_ids(api_key, playlist_id):
    """
    Fetches video IDs from a YouTube playlist using the YouTube API.

    Args:
        api_key (str): The YouTube API key.
        playlist_id (str): The YouTube playlist ID.

    Returns:
        list: A list of video IDs found in the playlist.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'contentDetails',
        'playlistId': playlist_id,
        'maxResults': 50,
        'key': api_key
    }
    video_ids = []
    while True:
        response = requests.get(base_url, params=params)
        
        # Handle errors in the API response
        if response.status_code != 200:
            print(f"Error fetching playlist items: {response.status_code} - {response.text}")
            return []
        response_json = response.json()
        if 'items' not in response_json:
            print("Error: 'items' not found in the API response")
            return []
        
        # Add video IDs to the list
        video_ids += [item['contentDetails']['videoId'] for item in response_json['items']]
        
        # Check for the nextPageToken for pagination
        if 'nextPageToken' in response_json:
            params['pageToken'] = response_json['nextPageToken']
        else:
            break
    return video_ids

def get_video_titles(api_key, video_ids):
    """
    Fetches video titles for the given video IDs using the YouTube API.

    Args:
        api_key (str): The YouTube API key.
        video_ids (list): A list of video IDs.

    Returns:
        list: A list of video titles corresponding to the given video IDs.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    video_titles = []

    # Process video IDs in batches of 50
    for i in range(0, len(video_ids), 50):
        batch_video_ids = video_ids[i:i + 50]
        params = {
            'part': 'snippet',
            'id': ','.join(batch_video_ids),
            'maxResults': 50,
            'key': api_key
        }
        response = requests.get(base_url, params=params)
        
        # Handle errors in the API response
        if response.status_code != 200:
            print(f"Error fetching video details: {response.status_code} - {response.text}")
            return []
        response_json = response.json()
        if 'items' not in response_json:
            print("Error: 'items' not found in the API response")
            return []
        
        # Add video titles to the list
        video_titles.extend([item['snippet']['title'] for item in response_json['items']])
    
    return video_titles