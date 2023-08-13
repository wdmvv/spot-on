import argparse


def cli_init():
    parser = argparse.ArgumentParser(description='Lets you download Spotify tracks from youtube',
    allow_abbrev=False)

    parser.add_argument('--type',
        help='Specify what to download album/playlist. Playlist by default',
        choices=['album', 'playlist'],
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

    parser.add_argument('--path',
        help='Download directory path, by default will create local directory \'Downloads\'',
        action='store',
        default='Downloads',
        nargs='?'
    )

    parser.add_argument('--precise',
        help='Precise search, might be considerably slower, False by default',
        type=bool,
        action=argparse.BooleanOptionalAction,
        #nargs='?'
    )

    parser.add_argument('--workers',
    help='Amount of threads to be launched for download, 5 by default',
        type=int,
        default=5,
        nargs='?'
    )
    
    return parser