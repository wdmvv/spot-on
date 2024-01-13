import os
import dotenv as dt
import cliargs
from spoton.connector import Connector

env = dt.load_dotenv()

if not env:
    with open('.env', 'w') as f:
        f.write('CLIENT_ID=\nCLIENT_SECRET=')

    print('.env was not detected, creating it - put CLIENT_ID and CLIENT_SECRET in')
    os._exit(1)

parser = cliargs.cli_init()
args = parser.parse_args()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

if not(client_id and client_secret):
    print('Failed to parse .env file, check validity')
    os._exit(1)

type = args.type
link = args.link
download_path = args.path
precise = args.precise
workers = args.workers
sideload_file = args.sideload

Connector = Connector(client_id, client_secret, workers)
Connector.process(type, link, download_path, precise, sideload_file)
