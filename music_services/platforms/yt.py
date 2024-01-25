import requests
import re
import os
import html
from dotenv import load_dotenv
from music_services.utils import extract_song_artist

load_dotenv()

def search_videos(search_term):
    api_key = os.environ['YT_API_KEY']
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={search_term}&key={api_key}"
    response = requests.get(url)
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    for item in response.json()['items']:
        if item['id']['kind'] == 'youtube#video' and pattern.search(search_term):
            track_info = extract_song_artist(item['snippet']['title'])

            result = {'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"}

            if track_info:
              result['track_name'] = html.unescape(track_info[1])
              result['track_artist'] = html.unescape(track_info[0])
            else:
              result['track_name'] = item['snippet']['title']
              result['track_artist'] = item['snippet']['channelTitle']

            return result
    return None
