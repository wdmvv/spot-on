'''
Module that is basically a bridge between main.py -> spotify.py -> download.py
It handles:
    Input link/id parsing
    Spotify connection
    Further downloads
'''

import utils
import spotify
import download


class Connector:
    def __init__(self, type, link, download_path, spotify_: spotify.Spotify):
        self.download_id = self.get_id(link)
        self.type = type

        self.downloader = download.Downloader(download_path)
        self.spotify_ = spotify_

        self.process()

    def get_id(self, link):
        download_id = utils.parse(link)
        return download_id

    def process(self):
        match self.type:
            case 'playlist':
                tracks = self.spotify_.get_playlist_tracks(self.download_id)
                todownload = spotify.build_pl_from_pl(tracks)
                self.downloader.batch_download(todownload)
            case 'album':
                tracks = self.spotify_.get_album_tracks(self.download_id)
                album = self.spotify_.get_album_info(self.download_id)
                todownload = spotify.build_pl_from_al(tracks, album)
                self.downloader.batch_download(todownload)

        
