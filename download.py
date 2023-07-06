'''
Module for working with yt-dlp and downloads managing, featuring:
    yt-dlp downloads
    metadata swapper
'''

import os
import logging
import yt_dlp
import requests
import music_tag

import spotify


def check_ddir(download_path):
    if not os.path.exists(f'{download_path}'):
        os.mkdir(f'{download_path}')

class Downloader:
    def __init__(self, download_path):
        #options for ytdlp         
        opts = {
            'default_search': 'auto',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-hide_banner'],
            'geo_bypass': True,
            'overwrites': True,
            #'logger': logging.Logger,
            'quiet': True
        }
        #structure for saving album covers as album_name - imgpath
        self.album_covers = {}
        self.ytdlp_opts = opts
        self.download_path = f'{download_path}'

        check_ddir(download_path)
    
    def batch_download(self, tracks: list[spotify.Track]):
        for i in tracks:
            self.download_track(i)
        logging.info(f'Cleaning up...')
        self.__cleanup()

    def download_track(self, track: spotify.Track):
        artists = ", ".join(track.track_artists)
        query = f'{track.track_name} - {artists} song'

        logging.info(f'Staring downloading {track.track_name}')

        savepath = os.path.join(self.download_path, track.track_name)
        opts = self.ytdlp_opts

        opts['outtmpl'] = savepath

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([query])

        self.change_metadata(savepath, track)

        logging.info(f'Downloaded track {track.track_name}')

    #needed for track cover
    def __get_album_image(self, track: spotify.Track):
        if track.album_name not in self.album_covers:
            filename = track.image_url.split('/')[-1]
            resp = requests.get(track.image_url)
            imgpath = os.path.join(self.download_path, filename) + '.jpg'

            if resp.status_code == 200:
                with open(imgpath, 'wb') as f:
                    f.write(resp.content)
            else:
                logging.error(f'Failed to download cover image for {track.track_name}')
                return None
            
            self.album_covers[track.album_name] = imgpath

        return self.album_covers[track.album_name]
    
    def change_metadata(self, filepath, track: spotify.Track):
        imgpath = self.__get_album_image(track)
        f = music_tag.load_file(filepath + '.mp3')
        if not f:
            logging.error(f'Failed to change metadata for {track.track_name} at {filepath}')
        else:
            f['artist'] = ', '.join(track.track_artists)
            f['album'] = track.album_name
            f['albumartist'] = ', '.join(track.album_artists)
            if imgpath:
                with open(imgpath, 'rb') as imgf:
                    f['artwork'] = imgf.read()
            else:
                logging.error(f'Failed to set album cover for {track.track_name}')
            f.save()

    #removing all album covers after downloading tracks
    def __cleanup(self):
        for i in self.album_covers:
            os.remove(self.album_covers[i])
        self.album_covers = {}



