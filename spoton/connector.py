'''
    Connector between spotify.py and download.py 
'''

import spoton.spotify as spotify
import spoton.downloader as downloader
import spoton.structs as structs


class Connector:
    def __init__(self,
        client_id: str,
        client_secret: str,
        ):
        '''
            client_id - spotify client id
            client_secret - spotify client secret
                ^ get both at https://developer.spotify.com/documentation/web-api/concepts/apps

        '''
        self.spotify_obj = spotify.Spotify(client_id, client_secret)
    
    def process(self, type: str, link: str, download_path: str, precise: bool):
        download_id = self.get_id(link)
        match type:
            case 'playlist':
                responses = self.spotify_obj.get_playlist(download_id)
                tracks = structs.tracks_from_playlist(responses)
            case 'album':
                responses = self.spotify_obj.get_album(download_id)
                album = self.spotify_obj.get_album_info(download_id)
                tracks = structs.tracks_from_album(responses, album)
            case _:
                raise(Exception('Invalid download type'))

        Downloader = downloader.Downloader(download_path)
        Downloader.batch_download(tracks, precise)


    def get_id(self, link):
        parts = link.split('/')
        return parts[-1] if parts[-1] != '' else parts[-2]