# -*- coding: UTF-8 -*-
#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000

import re,traceback,urlparse,urllib,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import dom_parser2
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123yts.net']
        self.base_link = 'http://www0.123yts.net/'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            scraper = cfscrape.create_scraper()
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
            r = cache.get(client.request, 1, search_url)
            r = client.parseDOM(r, 'div', {'id': 'movie-featured'})
            r = [(client.parseDOM(i, 'a', ret='href'),
                  re.findall('.+?elease:\s*(\d{4})</', i),
                  re.findall('<b><i>(.+?)</i>', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if
                 (cleantitle.get(i[2][0]) == cleantitle.get(title) and i[1][0] == year)]
            url = r[0][0]

            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            scraper = cfscrape.create_scraper()
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            scraper = cfscrape.create_scraper()
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            try:
                clean_title = cleantitle.geturl(url['tvshowtitle'])+'-season-%d' % int(season)
                search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
                r = cache.get(client.request, 1, search_url)
                r = client.parseDOM(r, 'div', {'id': 'movie-featured'})
                r = [(client.parseDOM(i, 'a', ret='href'),
                      re.findall('<b><i>(.+?)</i>', i)) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if
                     cleantitle.get(i[1][0]) == cleantitle.get(clean_title)]
                url = r[0][0]
            except:
                pass
            data = client.request(url)
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]

            return url[0][1]
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            scraper = cfscrape.create_scraper()
            sources = []
            r = cache.get(client.request, 1, url)
            try:
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    sources.append({
                        'source': host,
                        'quality': 'SD',
                        'language': 'en',
                        'url': url.replace('\/', '/'),
                        'direct': False,
                        'debridonly': False
                    })
                except:
                    pass
            except:
                pass
            r = client.parseDOM(r, 'div', {'class': 'server_line'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in r]
            if r:
                for i in r:
                    try:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        url = i[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if 'other'in host: continue
                        sources.append({
                            'source': host,
                            'quality': 'SD',
                            'language': 'en',
                            'url': url.replace('\/', '/'),
                            'direct': False,
                            'debridonly': False
                        })
                    except:
                        pass
            return sources
        except Exception:
            return

    def resolve(self, url):
        if self.base_link in url:
            url = client.request(url)
            v = re.findall('document.write\(Base64.decode\("(.+?)"\)', url)[0]
            b64 = base64.b64decode(v)
            url = client.parseDOM(b64, 'iframe', ret='src')[0]
        return url
