import music_services.platforms.tidal as tidal
import music_services.platforms.spotify as spotify
import music_services.platforms.yt as youtube

def get_source_track_info(id, platform):
    if platform == 'youtube':
      return youtube.search_videos(id)
    if platform == 'spotify':
      return spotify.get_track_info(id)
    if platform == 'tidal':
      return tidal.get_track_info(id)
    
def get_target_track_info(search_query, platform):
    if platform == 'youtube':
      return youtube.search_videos(search_query)
    if platform == 'spotify':
      return spotify.search_for_track(search_query)
    if platform == 'tidal':
      return tidal.search_for_track(search_query)