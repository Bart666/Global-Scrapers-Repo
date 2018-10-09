# -*- coding: utf-8 -*-

#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000


import re,urllib,urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['imdark.com']
        self.base_link = 'http://imdark.com'
        self.search_link = '/?s=%s&lang=en'
        self.ajax_link = '/wp-admin/admin-ajax.php'
       

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None

  

    def sources(self, url, hostDict, locDict):
        sources = []

        try:
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            #query = urlparse.urljoin(self.base_link, self.ajax_link)            
            #post = urllib.urlencode({'action':'sufi_search', 'search_string': title})
            
            result = client.request(query)
            r = client.parseDOM(result, 'div', attrs={'id':'showList'})
            r = re.findall(r'<a\s+style="color:white;"\s+href="([^"]+)">([^<]+)', r[0])     
            r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and data['year'] in i[1]][0]
            url = r[0]                     
            result = client.request(url)
            r = re.findall(r'video\s+id="\w+.*?src="([^"]+)".*?data-res="([^"]+)',result,re.DOTALL)
            
            for i in r:                
                try:
                    q = source_utils.label_to_quality(i[1])
                    sources.append({'source': 'CDN', 'quality': q, 'language': 'en', 'url': i[0], 'direct': True, 'debridonly': False})                
                except:
                    pass

            return sources
        except Exception as e:
            return sources

    def resolve(self, url):
        return url
