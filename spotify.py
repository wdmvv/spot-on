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
            logging.fatal(f'Failed to fetch tracks for {playlist_id}')

        resp_json = json.loads(resp.content)
        out.append(resp_json)

        if resp_json['total'] <= 100:
            return out
        else:
            for i in range(1, resp_json['total'] // 100 + (resp_json['total'] % 100 > 0)):                
                url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i * 100}&limit=100'
                resp = requests.get(url, headers=self.header)

                if resp.status_code != 200:
                    logging.fatal(f'Failed to fetch tracks for {playlist_id}')

                resp_json = json.loads(resp.content)
                out.append(resp_json)
            return out

'''
Interface for each track, contains most information about track
Base response json endpoints:
response -> "items": [] - array of dicts
                "track"
                    "name" - track name #
                    "album"
                        "name" - album name #
                        "images" - array of dicts
                            0th element
                                "url" - album image url in 640px #
                        "artists": [] - array of dicts
                            "name" - album artist name #
                    "arists": [] - array of dicts
                        "name" - track artist name #
                    "duration_ms" - duration for filtering #

'''
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


#Wrapper for __playlist_builder to handle get_playlist_tracks() response list
def build_playlist(responses: list[dict]) -> list[Track]:
    out = []
    for resp in responses:
        out.extend(__playlist_builder(resp))
    return out

#Function for building list[Track] for further work, accepts json response from https://api.spotify.com/v1/playlists/{playlist_id}/tracks
def __playlist_builder(response) -> list[Track]:
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
