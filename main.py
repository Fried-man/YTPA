import requests
import re
import base64
import requests
from collections import defaultdict
from config import YOUTUBE_API_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def get_playlist_id(url):
    pattern = r'(?:list=)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_ids(api_key, playlist_id):
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
        if response.status_code != 200:
            print(f"Error fetching playlist items: {response.status_code} - {response.text}")
            return []
        response_json = response.json()
        if 'items' not in response_json:
            print("Error: 'items' not found in the API response")
            return []
        video_ids += [item['contentDetails']['videoId'] for item in response_json['items']]
        if 'nextPageToken' in response_json:
            params['pageToken'] = response_json['nextPageToken']
        else:
            break
    return video_ids

def get_video_titles(api_key, video_ids):
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    video_titles = []
    
    for i in range(0, len(video_ids), 50):
        batch_video_ids = video_ids[i:i + 50]
        params = {
            'part': 'snippet',
            'id': ','.join(batch_video_ids),
            'maxResults': 50,
            'key': api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error fetching video details: {response.status_code} - {response.text}")
            return []
        response_json = response.json()
        if 'items' not in response_json:
            print("Error: 'items' not found in the API response")
            return []
        video_titles.extend([item['snippet']['title'] for item in response_json['items']])
    
    return video_titles

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    }
    response = requests.post(auth_url, data=auth_data, headers=auth_header)

    if response.status_code != 200:
        response_json = response.json()
        if response.status_code == 400 and response_json.get('error') == 'invalid_client':
            print("Invalid client. Please check your client_id and client_secret.")
        else:
            print(f"Error obtaining Spotify access token: {response.status_code} - {response.text}")
        return None

    return response.json()['access_token']


def get_genres_for_track(spotify_access_token, track_title):
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

    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    response = requests.get(artist_url, headers=search_header)
    if response.status_code != 200:
        print(f"Error fetching artist details: {response.status_code} - {response.text}")
        return []

    artist = response.json()
    return artist['genres']

def main():
    playlist_url = input("Enter a YouTube Music playlist URL: ")
    playlist_id = get_playlist_id(playlist_url)

    if not playlist_id:
        print("Invalid URL")
        return
    
    video_ids = get_video_ids(YOUTUBE_API_KEY, playlist_id)
    if len(video_ids) == 0:
        return

    video_titles = get_video_titles(YOUTUBE_API_KEY, video_ids)

    genre_count = defaultdict(int)
    total_genres = 0

    spotify_access_token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    if spotify_access_token is None:
        return

    for title in video_titles:
        genres = get_genres_for_track(spotify_access_token, title)
        for genre in genres:
            genre_count[genre] += 1
            total_genres += 1

    ranked_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

    print("Genre percentages for the playlist:")
    for genre, count in ranked_genres:
        percentage = (count / total_genres) * 100
        print(f"{genre}: {percentage:.2f}%")

if __name__ == "__main__":
    main()