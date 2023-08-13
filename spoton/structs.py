'''
    Album & Track classes and everything related to them, which includes:
        * Album & Track classes which store all information about album and single track respectively
        * Parsing list[dict] response from endpoint/playlists or endpoint/albums into list[Track]
        * Building list[Track] from album response requires not only api response with elements in album, but also album info
'''
from dataclasses import dataclass
from typing import Optional

@dataclass
class Album:
    name: str
    artists: list[str]
    image_url: str
    total_tracks: int

@dataclass
class Track:
    track_name: str
    album_name: str
    image_url: str
    album_artists: list[str]
    track_artists: list[str]
    duration_ms: int
    disk_number: Optional[int] = None
    track_number: Optional[int] = None
    total_tracks: Optional[int] = None


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
        duration_ms = item['track']['duration_ms']

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
            duration_ms=duration_ms
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
        
        track_number = item['track_number'] if 'track_number' in item else None
        total_tracks = album.total_tracks
        disk_number = item['disk_number'] if 'disk_number' in item else None

        duration_ms = item['duration_ms']

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
            track_number=track_number,
            total_tracks=total_tracks,
            duration_ms=duration_ms
        ))

    return tracks