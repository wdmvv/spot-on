'''
    Module for downloading tracks based on list[Track] and swapping metadata after processing

    batch_download - download multiple tracks, precise search or not
    download_track - casual track download that relies on first youtube search result
    precise_download - filters by duration and chooses closest one
'''

import os
import spoton.structs as structs
import yt_dlp
import music_tag
import requests

import concurrent.futures as cf

class Downloader:
    def __init__(self, download_path: str, workers: int):
        self.ytdlp_options = {
            'default_search': 'auto',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'quiet': True,
            'noprogress': True,
            'nooverwrites': True,        
        }

        #structure for saving album covers as album_name: imgpath
        self.album_covers = {}
        self.download_path = f'{download_path}'
        self.__create_dir(download_path)


        self.pool = cf.ThreadPoolExecutor(max_workers=workers)


    def batch_download(self, tracks: list[structs.Track], precise=False):
        download_func = self.download_track
        if precise:
            download_func = self.precise_download

        for i in tracks:
            self.pool.submit(download_func, i)

        self.pool.shutdown(wait=True)
        self.__cleanup()
        
    def download_track(self, track: structs.Track):
        artists = ", ".join(track.track_artists)
        request_query = f'{artists} - {track.track_name} song HQ'

        savepath = os.path.join(self.download_path, track.track_name)
        ytdlp_options = self.ytdlp_options.copy()

        ytdlp_options['outtmpl'] = savepath
        with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
            ydl.download([request_query])
        self.__change_metadata(savepath, track)

    #has duration filter (kinda)
    def precise_download(self, track: structs.Track):
        artists = ", ".join(track.track_artists)
        request_query = f'{artists} - {track.track_name} song'

        ytdlp_options = self.ytdlp_options.copy()

        # to get first 7 results, if it was ytsearch then it would give single one only
        # why 7? because 10 was too high, 5 too low, although further finetuning is required
        ytdlp_options['default_search'] = 'ytsearch7'

        duration_s = track.duration_ms // 1000

        with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
            info = ydl.extract_info(request_query, download=False)

            if not info:
                raise(Exception(f'Failed to extract data for {track.track_name}'))
            else:
                entries = info['entries']
                entries.sort(key=lambda x, dur=duration_s:(abs(x['duration'] - dur), x['view_count']))

                url = entries[0]['webpage_url']

        ytdlp_options['default_search'] = 'auto'

        savepath = os.path.join(self.download_path, track.track_name)
        ytdlp_options['outtmpl'] = savepath

        with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
            ydl.download([url])
        
        self.__change_metadata(savepath, track)

    def __change_metadata(self, audio_path: str, track: structs.Track):
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
            if track.total_tracks:
                f['totaltracks'] = track.total_tracks

            f.save()
    
    def __get_album_image(self, track: structs.Track) -> str:
        if track.album_name not in self.album_covers:

            filename = f'{track.album_artists} - {track.album_name}'
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

    def __create_dir(self, path: str):
        if not os.path.exists(f'{path}'):
            os.mkdir(f'{path}')
  