'''
Module for working with all spotify stuff, includes: 
    Spotify connection & playlists/tracks access (Spotify class),
    Track object with necessary information (Track class),
    Parsing & formatting response into list of tracks
'''

import base64
import requests
import json
import logging

import utils


class Spotify:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cliend_id, cliend_secret):
        self.client_id = cliend_id
        self.client_secret = cliend_secret

        token = self.__get_auth_token()

        logging.info('Successfully connected to spotify')
        
        self.token = token
        self.header = {'Authorization': 'Bearer ' + self.token}
                
    def __get_auth_token(self):
        auth = f'{self.client_id}:{self.client_secret}'
        auth_bytes = auth.encode('utf-8')

        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        token_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        resp = requests.post(token_url, headers=headers, data=data)     
        resp_json = json.loads(resp.content)

        if resp.status_code != 200:
            logging.fatal('Failed to acquire auth token. Check CLIENT_ID and CLIENT_SECRET validity')

        try:
            token = resp_json['access_token']
        except BaseException:
            logging.fatal('Failed to acquire auth token. Check CLIENT_ID and CLIENT_SECRET validity')
            
        return token       #it will not be unbound, pyright's wrong. (logging.fatal will call sys.exit)

    def get_playlist_tracks(self, playlist_id) -> list[dict]:
        out = []

        #First request - if amount of tracks exceeds 100 then it will send next requests with offset i * 100 & limit 100
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset=0&limit=100'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            logging.fatal(f'Failed to fetch playlist tracks for {playlist_id}')

        resp_json = json.loads(resp.content)
        out.append(resp_json)

        if resp_json['total'] > 100:
            for i in range(1, resp_json['total'] // 100 + (resp_json['total'] % 100 > 0)):                
                url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i * 100}&limit=100'
                resp = requests.get(url, headers=self.header)

                if resp.status_code != 200:
                    logging.fatal(f'Failed to fetch playlist tracks for {playlist_id}')

                resp_json = json.loads(resp.content)
                out.append(resp_json)
        return out
    
    #function's literally get_playlist_tracks, only url was changed, must make it less boilerplate-ish later
    def get_album_tracks(self, album_id) -> list[dict]:
        out = []

        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?offset=0&limit=50'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            logging.fatal(f'Failed to fetch album tracks for {album_id}')

        resp_json = json.loads(resp.content)
        out.append(resp_json)

        if resp_json['total'] > 50:
            for i in range(1, resp_json['total'] // 50 + (resp_json['total'] % 50 > 0)):                
                url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?offset={i * 50}&limit=50'
                resp = requests.get(url, headers=self.header)

                if resp.status_code != 200:
                    logging.fatal(f'Failed to fetch album tracks for {album_id}')

                resp_json = json.loads(resp.content)
                out.append(resp_json)
        return out

    #information about album itself, provides name, image url, artists
    def get_album_info(self, album_id):
        url = f'https://api.spotify.com/v1/albums/{album_id}'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            logging.fatal(f'Failed to fetch information for album {album_id}')

        resp_json = json.loads(resp.content)
        artists = [i['name'] for i in resp_json['artists']]
        album = Album(
            resp_json['name'],
            artists,
            resp_json['images'][0]['url'],
        )
        return album

class Track:
    def __init__(self,
        track_name: str,
        album_name: str,
        image_url: str,
        album_artists: list[str],
        track_artists: list[str],
        duration_s: int):

        self.track_name = track_name
        self.album_name = album_name
        self.image_url = image_url
        self.album_artists = album_artists
        self.track_artists = track_artists
        self.duration_s = duration_s

#Not needed that much but I thought it is better than passing same 3 arguments separately
class Album:
    def __init__(self,
        name: str,
        artists: list[str],
        image_url: str,
        ):

        self.name = name
        self.artists = artists
        self.image_url = image_url


def build_pl_from_pl(responses: list[dict]) -> list[Track]:
    out = []
    for resp in responses:
        out.extend(__tracks_playlist_builder(resp))
    return out

def __tracks_playlist_builder(response) -> list[Track]:
    out = []
    for item in response['items']:

        name = item['track']['name']
        album_name = item['track']['album']['name']
        image_url = item['track']['album']['images'][0]['url']

        duration_ms = item['track']['duration_ms']
        duration_s = utils.ms_to_s(duration_ms)

        album_artists = []
        for art in item['track']['album']['artists']:
            album_artists.append(art['name'])

        track_artists = []
        for art in item['track']['artists']:
            track_artists.append(art['name'])
        
        out.append(Track(
            track_name=name,
            album_name=album_name,
            image_url=image_url,
            album_artists=album_artists,
            track_artists=track_artists,
            duration_s=duration_s
        ))
    return out

def build_pl_from_al(responses: list[dict], album: Album) -> list[Track]:
    out = []
    for resp in responses:
        out.extend(__tracks_album_builder(resp, album))
    return out

def __tracks_album_builder(response, album: Album) -> list[Track]:
    out = []
    for item in response['items']:
        
        name = item['name']

        track_artists = []
        for art in item['artists']:
            track_artists.append(art['name'])
        
        duration_ms = item['duration_ms']
        duration_s = utils.ms_to_s(duration_ms)

        out.append(Track(
            track_name=name,
            album_name=album.name,
            image_url=album.image_url,
            album_artists=album.artists,
            track_artists=track_artists,
            duration_s=duration_s
        ))

    return out
    