# -*- coding: UTF-8 -*-
#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['hackimdb.com']
		self.base_link = 'https://hackimdb.com'
		self.search_link = '/title/&%s'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = self.base_link + self.search_link % imdb
			return url
		except:
			return
			
	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			try:
				match = re.compile('<iframe .+?src=".+?rapidvideo(.+?)"').findall(r)
				for url in match: 
					url = 'https://www.rapidvideo' + url
					
					r = client.request(url)
					match = re.compile('<source src="(.+?)" type="video/mp4" title="(.+?)"').findall(r)
					for url, quality in match:
					
						sources.append({
							'source': 'RapidVideo',
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