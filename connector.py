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
    def __init__(self, link, download_path, spotify_: spotify.Spotify):
        self.playlist_id = self.get_id(link)

        self.downloader = download.Downloader(download_path)
        self.spotify_ = spotify_

        self.process()

    def get_id(self, link):
        playlist_id = utils.parse(link)
        return playlist_id

    def process(self):
        tracks = self.spotify_.get_playlist_tracks(self.playlist_id)
        playlist = spotify.build_playlist(tracks)
        self.downloader.batch_download(playlist)

        
