import sys
from music_services.search import get_source_track_info, get_target_track_info
from music_services.utils import url_sanitiser

platforms = ['spotify', 'tidal', 'youtube']
  
def cli_search():
  target_index = int(input('Which platform would you like to search on? Spotify (1), Tidal (2) or YouTube (3): ')) - 1
  search_query = input('Enter song and/or artist name: ')

  if platforms[target_index] and len(search_query) > 0:
    result = get_target_track_info(search_query, platforms[target_index])
    print(f'Found {result["track_name"]} by {result["track_artist"]}')
    print(f'Here is your {platforms[target_index]} link: {result["url"]}')

  sys.exit()

def cli_convert(url_info):
    source_platform = url_info['source_platform']
    source_track_info = get_source_track_info(url_info['id'], source_platform)

    if source_track_info == None:
        user_input = input('No track found. Would you like to search for a song? (Yes/No/Y/N): ').lower()
        if user_input == 'yes' or user_input == 'y':
          cli_search()
        else:
          sys.exit()

    possible_platforms = [platform for platform in platforms if platform != source_platform]
    search_query = f'{source_track_info["track_name"]} {source_track_info["track_artist"]}'

    print(f'That is a {source_platform} link for {source_track_info["track_name"]} by {source_track_info["track_artist"]}')

    target_index = int(input(f'Convert to {possible_platforms[0]} (1) or {possible_platforms[1]} (2) link: ')) - 1
    target_platform = possible_platforms[target_index]

    result = get_target_track_info(search_query, target_platform)

    print(f'Here is your {target_platform} link: {result["url"]}')

    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
      if (sys.argv[1] =='--search' or sys.argv[1] == '-s'):
        cli_search()

      url_info = url_sanitiser(sys.argv[1])

      if url_info == None:
        user_input = input('Invalid or no URL found. Would you like to search for a song? (Yes/No/Y/N): ').lower()
        if user_input == 'yes' or user_input == 'y':
          cli_search()
      else:
        cli_convert(url_info)

    else:
        print('--- Usage ---\n\nSupports Spotify, Tidal and Youtube URLs\n\nConvert music URL:  musiclinkconvert.py <music_url>\n\nSearch for music URL:  musiclinkconvert.py --search or musiclinkconvert.py -s')
        sys.exit()
