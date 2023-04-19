import requests
import re
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
    params = {
        'part': 'snippet',
        'id': ','.join(video_ids),
        'maxResults': 100,
        'key': api_key
    }
    response = requests.get(base_url, params=params).json()
    return [item['snippet']['title'] for item in response['items']]

def main():
    playlist_url = input("Enter a YouTube Music playlist URL: ")
    playlist_id = get_playlist_id(playlist_url)

    if not playlist_id:
        print("Invalid URL")
    else:
        video_ids = get_video_ids(YOUTUBE_API_KEY, playlist_id)
        if len(video_ids) == 0:
            return

        video_titles = get_video_titles(YOUTUBE_API_KEY, video_ids)

        # This part requires you to integrate with a music metadata API, like Spotify.
        # You can follow the Spotify API documentation to implement this part.
        # https://developer.spotify.com/documentation/web-api/

        # For demonstration purposes, let's assume you have a function called
        # `get_genres_for_track` that takes a track title and returns a list of genres.
        # def get_genres_for_track(spotify_access_token, track_title): ...

        genre_count = defaultdict(int)
        total_genres = 0

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