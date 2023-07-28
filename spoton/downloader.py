'''
    Module for downloading tracks based on list[Track] and swapping metadata after processing
'''

import os
import spoton.structs as structs
import yt_dlp
import music_tag
import requests


class Downloader:
    def __init__(self, download_path):

        self.ytdlp_options = {
            'default_search': 'ytsearch',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-hide_banner'],
            'geo_bypass': True,
            'overwrites': True,
            'quiet': True
        }

        #structure for saving album covers as album_name: imgpath
        self.album_covers = {}

        self.download_path = f'{download_path}'
        self.__create_dir(download_path)

    def batch_download(self, tracks: list[structs.Track]):
        for i in tracks:
            self.download_track(i)
        self.__cleanup()
    
    def download_track(self, track: structs.Track):
        artists = ", ".join(track.track_artists)
        request_query = f'{artists} - {track.track_name} song HD'

        savepath = os.path.join(self.download_path, track.track_name)
        ytdlp_options = self.ytdlp_options

        ytdlp_options['outtmpl'] = savepath

        with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
            ydl.download([request_query])

        self.__change_metadata(savepath, track)

    def __change_metadata(self, audio_path, track: structs.Track):
        imgpath = self.__get_album_image(track)
        f = music_tag.load_file(audio_path + '.mp3')
        if not f:
            raise(Exception(f'Failed to change metadata for {track.track_name} at {audio_path}'))
        else:
            f['artist'] = ', '.join(track.track_artists)
            f['album'] = track.album_name
            f['albumartist'] = ', '.join(track.album_artists)
            if imgpath:
                with open(imgpath, 'rb') as imgf:
                    f['artwork'] = imgf.read()
            else:
                raise(Exception(f'Failed to set album cover for {track.track_name}'))
            
            if track.disk_number:
                f['discnumber'] = track.disk_number
            if track.track_number:
                f['tracknumber'] = track.track_number

            f.save()
    
    def __get_album_image(self, track: structs.Track) -> str:
        if track.album_name not in self.album_covers:
            filename = track.image_url.split('/')[-1]
            resp = requests.get(track.image_url)
            imgpath = os.path.join(self.download_path, filename) + '.jpg'

            if resp.status_code == 200:
                with open(imgpath, 'wb') as f:
                    f.write(resp.content)
            else:
                raise(Exception(f'Failed to download cover image for {track.track_name}'))
            
            self.album_covers[track.album_name] = imgpath

        return self.album_covers[track.album_name]

    def __cleanup(self):
        for i in self.album_covers:
            os.remove(self.album_covers[i])
        self.album_covers = {}

    def __create_dir(self, path):
        if not os.path.exists(f'{path}'):
            os.mkdir(f'{path}')
  