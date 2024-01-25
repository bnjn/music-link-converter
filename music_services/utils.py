import re

def extract_song_artist(string):
    string = re.sub(r'\[.*?\]', '', string)  # Remove anything in square brackets
    pattern = re.compile(r'^(.+) - (.+)')
    match = pattern.match(string)
    if match:
        return match.groups()
    else:
        return None
    
def url_sanitiser(url):
    tidal_link_pattern = re.compile(r'https?://(?:www\.)?tidal\.com/browse/track/\d+')
    spotify_link_pattern = re.compile(r'https://open\.spotify\.com/track/[a-zA-Z0-9]+')
    youtube_link_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+')

    tidal_link = re.search(tidal_link_pattern, url)
    spotify_link = re.search(spotify_link_pattern, url)
    youtube_link= re.search(youtube_link_pattern, url)

    if youtube_link:
      return { 'source_platform': 'youtube', 'id': url }
        
    if tidal_link:
      track_id = re.search(r'\d+', url)
      return { 'source_platform': 'tidal', 'id': track_id.group(0)}

    if spotify_link:
      track_id = re.search(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', url)
      return { 'source_platform': 'spotify', 'id': track_id.group(1) }

    return None