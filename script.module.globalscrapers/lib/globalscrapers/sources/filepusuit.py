#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils 
class source:
    def __init__(self):
        self.priority = 1                           
        self.language = ['en']                      
        self.domains = ['filepursuit.com']           
        self.base_link = 'https://filepursuit.com'  
        self.search_link = '/search5/%s/' 
 
    def movie(self, imdb, title, localtitle, aliases, year):
       
        
       
        try:
           
            title = cleantitle.geturl(title)
            
            url = '%s+%s' % (title,year)
           
           
            return url
        except:
            return
           
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        
        try:
           
           
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
           
           
            tvshowtitle = url
           
           
           
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
           
            
           
            url = '%s+s%se%s' % (tvshowtitle,str(season),str(episode))
           
           
            return url
        except:
            return
 
 
    def sources(self, url, hostDict, hostprDict):
       
      
       
        try:
            sources = []
 
           
            query = url
 
           
 
            url = self.base_link + self.search_link % query
 
 
            r = client.request(url)
 
 
            try:
               
 
                match = re.compile('data-clipboard-text="(.+?)"').findall(r)
               
               
                for url in match:
               
               
                    if '2160' in url: quality = '4K'
                    elif '4k' in url: quality = '4K'
                    elif '1080' in url: quality = '1080p'
                    elif '720' in url: quality = 'HD'
                    elif '480' in url: quality = 'SD' 
                    else: quality = 'SD'
                   
                   
                    sources.append({
                        'source': 'Direct', 
                        'quality': quality, 
                        'language': 'en',   
                        'url': url,         
                        'direct': False,   
                        'debridonly': False 
                    })
            except:
                return
        except Exception:
            return
           
    
           
        return sources
 
    def resolve(self, url):
        return url