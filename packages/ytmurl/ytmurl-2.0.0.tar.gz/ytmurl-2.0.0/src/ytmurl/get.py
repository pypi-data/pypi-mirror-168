from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
import logging
import json

def get(query, duration=None, logger=logging.getLogger()):
    # sanitize query
    query = query.replace('-', '')

    # ytm search
    ytmusic = YTMusic()
    results = ytmusic.search(query.replace('-', ''))
    logger.debug(f'Got results from ytmusic: {json.dumps(results)}')

    def in_range(v, range):
        return v >= range[0] and v <= range[1]

    # select song
    def select_song(results):
        for r in results:
            if all([
                r['category'] in ['Top result', 'Songs', 'Videos'],
                r['resultType'] in ('song', 'video'),
                duration is None or ('duration_seconds' in r and in_range(r['duration_seconds'], duration)),
            ]):
                return r['videoId']
        raise Exception(f'No match for "{query}"')

    songId = select_song(results)
    logger.info(f'Retrieved Song Id: {songId}')

    # get url with yt-dlp
    ydl_opts = {
        'format' : 'bestaudio',
        'logger' : logger,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={songId}', download=False)
        info = ydl.sanitize_info(info)

    logger.debug(f'Got json: {json.dumps(info)}')

    url = info['url']

    logger.info(f'Got URL: {url}')
    return url
