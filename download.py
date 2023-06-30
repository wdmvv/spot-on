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

        self.ytdlp_opts = opts
        self.download_path = f'{download_path}'

        check_ddir(download_path)
    
    def batch_download(self, tracks: list[spotify.Track]):
        for i in tracks:
            self.download_track(i)

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
    def __download_image(self, link, track_name):
        filename = link.split('/')[-1]
        resp = requests.get(link)
        imgpath = os.path.join(self.download_path, filename) + '.jpg'

        if resp.status_code == 200:
            with open(imgpath, 'wb') as f:
                f.write(resp.content)
        else:
            logging.error(f'Failed to download cover image for {track_name}')
            return None

        return imgpath
    
    def change_metadata(self, filepath, track: spotify.Track):
        imgpath = self.__download_image(track.image_url, track.track_name)
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
        if imgpath:
            os.remove(imgpath)


