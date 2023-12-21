import urllib.parse
import requests
import json
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token_api(client_id, secret):
    url = 'https://accounts.spotify.com/api/token'
    header = {'content-Type': 'application/x-www-form-urlencoded'}
    request_data = f'grant_type=client_credentials&client_id={client_id}&client_secret={secret}'
    try:
        response = requests.post(url=url, headers=header, data=request_data)
        token = json.loads(response.text)
        token['time_accessed'] = time.time()
        return token
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)


def store_access_token(token):
    if 'error' in token:
        raise Exception(f'Spotify API error: {token["error"]} - {token["error_description"]}')

    if not os.path.isdir('auth_tokens'):
        os.mkdir('auth_tokens')

    if isinstance(token, dict):
        with open('auth_tokens/spotify_token', 'w') as data:
            data.write(json.dumps(token))
    else:
        raise TypeError('Token is not a dict')


def get_access_token():
    if os.path.exists('auth_tokens/spotify_token'):
        with open('auth_tokens/spotify_token', 'r') as data:
            token = json.loads(data.read())
            if (int(token['time_accessed'])) + 3600 > time.time():
                return f'{token["token_type"]}  {token["access_token"]}'
            else:
                token = get_access_token_api(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_SECRET'])
                store_access_token(token)
                return f'{token["token_type"]}  {token["access_token"]}'
    else:
        token = get_access_token_api(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_SECRET'])
        store_access_token(token)
        return f'{token["token_type"]}  {token["access_token"]}'


def search_for_track(search_string):
    encoded_query = urllib.parse.quote(search_string, safe='')
    search_url = f'https://api.spotify.com/v1/search?q={encoded_query}&type=track'
    auth_header = {"Authorization": get_access_token()}
    try:
        response = requests.get(url=search_url, headers=auth_header)
        top_result = json.loads(response.text)['tracks']['items'][0]
        track = {
            'track_name': top_result['name'],
            'track_artist': top_result['artists'][0]['name'],
            'spotify_url': top_result['external_urls']['spotify'],

        }
        return track
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)


def get_track_info(track_id):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    auth_header = {"Authorization": get_access_token()}
    try:
        response = requests.get(url=url, headers=auth_header)
        result = json.loads(response.text)
        track = {
            'track_name': result['name'],
            'track_artist': result['artists'][0]['name']
        }
        return track
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)

