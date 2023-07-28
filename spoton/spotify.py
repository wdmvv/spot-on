'''
    Spotify class, which:
        * Connects to Spotify with client id and client secret
        * Enables to get album/playlist tracks into list[dict] structure (parsed further in structs.py)
        * Allows to get album information to get additional data on album
'''

import base64
import requests
import json
import spoton.structs as structs


class Spotify:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        self.auth_token = self.__get_auth_token()
        self.header = {'Authorization': 'Bearer ' + self.auth_token}
   
    def __get_auth_token(self) -> str:
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
            raise(Exception('Failed to acquire auth token. Check CLIENT_ID and CLIENT_SECRET validity'))
        try:
            token = resp_json['access_token']
        except BaseException:
            raise(Exception('Failed to acquire auth token. Check CLIENT_ID and CLIENT_SECRET validity'))

        
        return token

    def get_playlist(self, playlist_id: str) -> list[dict]:
        out = []

        #First request - if amount of tracks exceeds 100 then it will send next requests with offset i * 100 & limit 100
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset=0&limit=100'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            raise(Exception(f'Failed to fetch playlist tracks for {playlist_id}'))

        resp_json = json.loads(resp.content)
        out.append(resp_json)

        if resp_json['total'] > 100:
            for i in range(1, resp_json['total'] // 100 + (resp_json['total'] % 100 > 0)):                
                url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i * 100}&limit=100'
                resp = requests.get(url, headers=self.header)

                if resp.status_code != 200:
                    raise(Exception(f'Failed to fetch playlist tracks for {playlist_id}'))
                
                resp_json = json.loads(resp.content)
                out.append(resp_json)

                resp.close()
        return out

    def get_album(self, album_id: str) -> list[dict]:
        out = []

        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?offset=0&limit=50'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            raise(Exception(f'Failed to fetch album tracks for {album_id}'))

        resp_json = json.loads(resp.content)
        out.append(resp_json)

        if resp_json['total'] > 50:
            for i in range(1, resp_json['total'] // 50 + (resp_json['total'] % 50 > 0)):                
                url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?offset={i * 50}&limit=50'
                resp = requests.get(url, headers=self.header)

                if resp.status_code != 200:
                    raise(Exception(f'Failed to fetch album tracks for {album_id}'))

                resp_json = json.loads(resp.content)
                out.append(resp_json)
        return out
    
    def get_album_info(self, album_id: str) -> structs.Album:
        url = f'https://api.spotify.com/v1/albums/{album_id}'

        resp = requests.get(url, headers=self.header)
        if resp.status_code != 200:
            raise(Exception(f'Failed to fetch information for album {album_id}'))

        resp_json = json.loads(resp.content)
        artists = [i['name'] for i in resp_json['artists']]

        album = structs.Album(
            resp_json['name'],
            artists,
            resp_json['images'][0]['url'],
        )

        return album
