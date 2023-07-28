'''
    Album & Track classes and everything related to them, which includes:
        * Album & Track classes which store all information about album and single track respectively
        * Parsing list[dict] response from endpoint/playlists or endpoint/albums into list[Track]
        * Building list[Track] from album response requires not only api response with elements in album, but also album info
'''

class Album:
    def __init__(self,
        name: str,
        artists: list[str],
        image_url: str,
        ):

        self.name = name
        self.artists = artists
        self.image_url = image_url

class Track:
    def __init__(self,
        track_name: str,
        album_name: str,
        image_url: str,
        album_artists: list[str],
        track_artists: list[str],
        disk_number=None,
        track_number=None):

        self.track_name = track_name
        self.album_name = album_name
        self.image_url = image_url
        self.album_artists = album_artists
        self.track_artists = track_artists
        self.disk_number = disk_number
        self.track_number = track_number


def tracks_from_playlist(responses: list[dict]) -> list[Track]:
    tracks = []
    for resp in responses:
        tracks.extend(__playlist_tracks_builder(resp))
    return tracks

def __playlist_tracks_builder(response) -> list[Track]:
    tracks = []
    for item in response['items']:

        name = item['track']['name']
        album_name = item['track']['album']['name']
        image_url = item['track']['album']['images'][0]['url']

        album_artists = []
        for art in item['track']['album']['artists']:
            album_artists.append(art['name'])

        track_artists = []
        for art in item['track']['artists']:
            track_artists.append(art['name'])
        
        tracks.append(Track(
            track_name=name,
            album_name=album_name,
            image_url=image_url,
            album_artists=album_artists,
            track_artists=track_artists,
        ))
    return tracks

def tracks_from_album(responses: list[dict], album: Album) -> list[Track]:
    tracks = []
    for resp in responses:
        tracks.extend(__album_tracks_builder(resp, album))
    return tracks

def __album_tracks_builder(response, album: Album) -> list[Track]:
    tracks = []
    for item in response['items']:
        name = item['name']

        track_number = item['track_number']
        disk_number = item['disk_number']

        track_artists = []
        for art in item['artists']:
            track_artists.append(art['name'])

        tracks.append(Track(
            track_name=name,
            album_name=album.name,
            image_url=album.image_url,
            album_artists=album.artists,
            track_artists=track_artists,
            disk_number=disk_number,
            track_number=track_number
        ))

    return tracks