# -*- coding: utf-8 -*-

#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animeultima.io']
        self.base_link = 'https://www4.animeultima.eu/'
        self.search_link = '/search.html?searchquery=%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']

            t = cleantitle.get(tvshowtitle)

            q = self.search_link % (urllib.quote_plus(tvshowtitle))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)

            r = client.parseDOM(r, 'ol', attrs = {'id': 'searchresult'})[0]
            r = client.parseDOM(r, 'h2')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.sub('<.+?>|</.+?>','', i[1])) for i in r]
            r = [i for i in r if t == cleantitle.get(i[1])]
            r = r[-1][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            num = str(num)

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            r = client.parseDOM(r, 'tr', attrs = {'class': ''})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'td', attrs = {'class': 'epnum'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if num == i[1]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            locDict = [i[0] for i in hostDict]

            result = client.request(url)

            links = []

            try:
                r = client.parseDOM(result, 'div', attrs = {'class': 'player-embed'})[0]
                r = client.parseDOM(r, 'iframe', ret='src')[0]
                links += [(r, url)]
            except:
                pass

            try:
                r = client.parseDOM(result, 'div', attrs = {'class': 'generic-video-item'})
                r = [(i.split('</div>', 1)[-1].split()[0], client.parseDOM(i, 'a', ret='href', attrs = {'rel': '.+?'})) for i in r]
                links += [(i[0], i[1][0]) for i in r if i[1]]
            except:
                pass

            for i in links:
                try:
                    try: host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i[0].strip().lower()).netloc)[0]
                    except: host = i[0].lower()
                    host = host.rsplit('.', 1)[0]
                    if not host in locDict: raise Exception()
                    host = [x[1] for x in hostDict if x[0] == host][0]
                    host = host.encode('utf-8')

                    url = i[1]
                    url = urlparse.urljoin(self.base_link, url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')

            url = client.parseDOM(result, 'div', attrs = {'class': 'player-embed'})[0]
            url = client.parseDOM(url, 'iframe', ret='src')[0]

            return url
        except:
            return


