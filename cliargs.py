import argparse


def cli_init():
    parser = argparse.ArgumentParser(description='Lets you download Spotify tracks from youtube',
    allow_abbrev=False)

    parser.add_argument('type',
        help='Specify what to download album/playlist. Playlist by default',
        type=str,
        action='store',
        default='playlist',
        nargs='?'
    )

    parser.add_argument('link',
        help='Main link parameter, can be either link or id',
        type=str,
        action='store',
        default=''
        )

    parser.add_argument('download_path',
        help='Download directory path, by default will create local directory \'Downloads\'',
        action='store',
        default='Downloads',
        nargs='?'
    )
    
    return parser