import logging
import dotenv, os

import logs
import cliargs
import spotify
import connector

logs.Logger()

parser = cliargs.cli_init()
args = parser.parse_args()

env = dotenv.load_dotenv()

if not env:
    f = open('.env', 'w')
    f.write('CLIENT_ID=\n')
    f.write('CLIENT_SECRET=')
    f.close()
    logging.fatal('.env was not detected, created it - fill in CLIENT_ID and CLIENT_SECRET')

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

#very h, really
spotify_ = spotify.Spotify(client_id, client_secret)

link = args.link
download_path = args.download_path

connector.Connector(link, download_path, spotify_)