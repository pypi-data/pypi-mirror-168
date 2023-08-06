__version__ = "2.0.0"

from .get import *
import argparse
import os
import sys

def main():
    # argparse
    parser = argparse.ArgumentParser(description = 'searches youtube music and prints audio url')
    parser.add_argument('query', help='query string containing title, artist, etc')
    parser.add_argument('-l', '--log-file', dest='log', default='', help='log file to append to')
    parser.add_argument('-d', '--duration', metavar=('FROM', 'TO'), nargs=2, type=int, default=None, help='duration range of song in seconds, inclusive')
    args = parser.parse_args()

    # logging setup
    if args.log != '':
        os.makedirs(os.path.dirname(args.log), exist_ok=True)
        logging.basicConfig(filename=args.log, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    else:
        logging.basicConfig(level=logging.ERROR)

    # log the command
    logging.info(f'ytmurl {" ".join(sys.argv)}')

    try:
        print(get(args.query, duration=args.duration, logger=logging.getLogger()))
    except Exception:
        logging.exception('YtmUrlException')


