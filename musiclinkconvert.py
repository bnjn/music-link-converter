import re
import lib.tidal as tidal
import lib.spotify as spotify
import sys


def convert(url):
    tidal_link_pattern = re.compile(r'https?://(?:www\.)?tidal\.com/browse/track/\d+')
    spotify_link_pattern = re.compile(r'https://open\.spotify\.com/track/[a-zA-Z0-9]+')
    tidal_link = re.search(tidal_link_pattern, url)
    spotify_link = re.search(spotify_link_pattern, url)
    if tidal_link:
        track_id = re.search(r'\d+', url)
        if track_id:
            track_info = tidal.get_track_info(track_id.group(0))
            print(f'That is a Tidal link for {track_info["track_name"]} by {track_info["track_artist"]}')
            spotify_result = spotify.search_for_track(f'{track_info["track_name"]} {track_info["track_artist"]}')
            print(f"Here is your Spotify link: {spotify_result['spotify_url']}")
        return
    if spotify_link:
        track_id = re.search(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', url)
        if track_id:
            track_info = spotify.get_track_info(track_id.group(1))
            print(f'That is a Spotify link for {track_info["track_name"]} by {track_info["track_artist"]}')
            tidal_result = tidal.search_for_track(f'{track_info["track_name"]} {track_info["track_artist"]}')
            print(f"Here is your Tidal link: {tidal_result['tidal_url']}")
        return
    print('That is not a valid music link')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert(sys.argv[1])
    else:
        print('Usage: musiclinkconvert.py <music_url>')
