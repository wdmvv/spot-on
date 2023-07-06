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
    logging.fatal('.env was not detected, creating it - fill in CLIENT_ID and CLIENT_SECRET')

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

#very h, really
spotify_ = spotify.Spotify(client_id, client_secret)

#Download type, album or playlist
#I know it should not be like this but currently I have no idea how to improve this
type = args.type
link = args.link
download_path = args.download_path

connector.Connector(type, link, download_path, spotify_)