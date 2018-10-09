# -*- coding: utf-8 -*-

#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000


import urllib,urlparse,json

from resources.lib.modules import control
from resources.lib.modules import cleantitle

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en', 'de', 'fr', 'ko', 'pl', 'pt', 'ru']
        self.domains = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            return urllib.urlencode({'imdb': imdb, 'title': title, 'localtitle': localtitle,'year': year})
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            return urllib.urlencode({'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'year': year})
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url.update({'premiered': premiered, 'season': season, 'episode': episode})
            return urllib.urlencode(url)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            content_type = 'episode' if 'tvshowtitle' in data else 'movie'

            years = (data['year'], str(int(data['year'])+1), str(int(data['year'])-1))

            if content_type == 'movie':
                title = cleantitle.get(data['title'])
                localtitle = cleantitle.get(data['localtitle'])
                ids = [data['imdb']]

                r = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "originaltitle", "file"]}, "id": 1}' % years)
                r = unicode(r, 'utf-8', errors='ignore')
                r = json.loads(r)['result']['movies']

                r = [i for i in r if str(i['imdbnumber']) in ids or title in [cleantitle.get(i['title'].encode('utf-8')), cleantitle.get(i['originaltitle'].encode('utf-8'))]]
                r = [i for i in r if not i['file'].encode('utf-8').endswith('.strm')][0]

                r = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["streamdetails", "file"], "movieid": %s }, "id": 1}' % str(r['movieid']))
                r = unicode(r, 'utf-8', errors='ignore')
                r = json.loads(r)['result']['moviedetails']
            elif content_type == 'episode':
                title = data['tvshowtitle']
                localtitle = data['localtvshowtitle']
                season, episode = data['season'], data['episode']

                r = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title"]}, "id": 1}' % years)
                r = unicode(r, 'utf-8', errors='ignore')
                r = json.loads(r)['result']['tvshows']

                r = [i for i in r if title in (i['title'].encode('utf-8'))][0]

                r = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
                r = unicode(r, 'utf-8', errors='ignore')
                r = json.loads(r)['result']['episodes']

                r = [i for i in r if not i['file'].encode('utf-8').endswith('.strm')][0]

                r = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["streamdetails", "file"], "episodeid": %s }, "id": 1}' % str(r['episodeid']))
                r = unicode(r, 'utf-8', errors='ignore')
                r = json.loads(r)['result']['episodedetails']

            url = r['file'].encode('utf-8')

            try: quality = int(r['streamdetails']['video'][0]['width'])
            except: quality = -1

            if quality > 1920: quality = '2160p'
            if quality >= 1920: quality = '1080p'
            if 1280 <= quality < 1900: quality = 'HD'
            if quality < 1280: quality = 'HQ'

            info = []

            try:
                f = control.openFile(url) ; s = f.size() ; f.close()
                s = '%.2f GB' % (float(s)/1024/1024/1024)
                info.append(s)
            except: pass

            try:
                c = r['streamdetails']['video'][0]['codec']
                if c == 'avc1': c = 'h264'
                info.append(c)
            except: pass

            try:
                ac = r['streamdetails']['audio'][0]['codec']
                if ac == 'dca': ac = 'dts'
                if ac == 'dtshd_ma': ac = 'dts-hd ma'
                info.append(ac)
            except: pass

            try:
                ach = r['streamdetails']['audio'][0]['channels']
                if ach == 1: ach = 'mono'
                if ach == 2: ach = '2.0'
                if ach == 6: ach = '5.1'
                if ach == 8: ach = '7.1'
                info.append(ach)
            except: pass
            
            info = ' | '.join(info)
            info = info.encode('utf-8')

            sources.append({'source': '0', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'local': True, 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


