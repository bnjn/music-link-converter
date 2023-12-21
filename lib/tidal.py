import base64
import urllib.parse
import requests
import time
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token_api(client_id, secret):
    auth_data = base64.b64encode(f'{client_id}:{secret}'.encode()).decode()
    url = 'https://auth.tidal.com/v1/oauth2/token'
    auth_header = {'Authorization': f'Basic {auth_data}', 'content-type': 'application/x-www-form-urlencoded'}
    request_data = f'grant_type=client_credentials'
    try:
        response = requests.post(url=url, headers=auth_header, data=request_data)
        token = json.loads(response.text)
        token['time_accessed'] = time.time()
        return token
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)


def store_access_token(token):
    if 'error' in token:
        raise Exception(f'Tidal API error: {token["error"]} - {token["error_description"]}')

    if not os.path.isdir('auth_tokens'):
        os.mkdir('auth_tokens')

    if isinstance(token, dict):
        with open('auth_tokens/tidal_token', 'w') as data:
            data.write(json.dumps(token))
    else:
        raise TypeError('Token is not a dict')


def get_access_token():
    if os.path.exists('auth_tokens/tidal_token'):
        with open('auth_tokens/tidal_token', 'r') as data:
            token = json.loads(data.read())

            if (int(token['time_accessed'])) + 86400 > time.time():
                return f'{token["token_type"]} {token["access_token"]}'
            else:
                token = get_access_token_api(os.environ['TIDAL_CLIENT_ID'], os.environ['TIDAL_SECRET'])
                store_access_token(token)
                return f'{token["token_type"]} {token["access_token"]}'
    else:
        token = get_access_token_api(os.environ['TIDAL_CLIENT_ID'], os.environ['TIDAL_SECRET'])
        store_access_token(token)
        return f'{token["token_type"]} {token["access_token"]}'


def search_for_track(search_string):
    encoded_query = urllib.parse.quote(search_string, safe='')
    params = 'type=TRACKS&offset=0&limit=1&countryCode=GB&popularity=WORLDWIDE'
    search_url = f'https://openapi.tidal.com/search?query={encoded_query}&{params}'
    headers = {
        "Authorization": get_access_token(),
        "accept": "application/vnd.tidal.v1+json",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    try:
        response = requests.get(url=search_url, headers=headers)
        result = json.loads(response.text)['tracks'][0]
        if 'resource' in result:
            result = result['resource']
            track = {
                'track_name': result['title'],
                'track_artist': result['artists'][0]['name'],
                'tidal_url': f'https://tidal.com/browse/track/{result["id"]}'
            }
            return track
        else:
            logging.info(response.text)
            print('Track not found or currently restricted by copyright :(')
            raise SystemExit

    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)


def get_track_info(track_id):
    params = 'countryCode=GB'
    url = f'https://openapi.tidal.com/tracks/{track_id}?{params}'
    headers = {
        "Authorization": get_access_token(),
        "accept": "application/vnd.tidal.v1+json",
        "Content-Type": "application/vnd.tidal.v1+json"
    }
    try:
        response = requests.get(url=url, headers=headers)
        result = json.loads(response.text)['resource']
        track = {
            'track_name': result['title'],
            'track_artist': result['artists'][0]['name']
        }
        return track
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)
