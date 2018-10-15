# -*- coding: UTF-8 -*-
#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000

import base64
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
		self.domains = ['sockshare.ac']
		self.base_link = 'http://sockshare.ac'
		self.search_link = '/search-movies/%s.html'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			q = cleantitle.geturl(title)
			q2 = q.replace('-','+')
			url = self.base_link + self.search_link % q2
			r = client.request(url)
			match = re.compile('<a class="title" href="(.+?)-'+q+'\.html"').findall(r)
			for url in match:
				url = '%s-%s.html' % (url,q)
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
			
			q = url + '-season-' + season
			q2 = url.replace('-','+')
			url = self.base_link + self.search_link % q2
			r = client.request(url)
			match = re.compile('<a class="title" href="(.+?)-'+q+'\.html"').findall(r)
			for url in match:
				url = '%s-%s.html' % (url,q)
				r = client.request(url)
				match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
				for url in match:
					return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			try:
				match = re.compile('<img src="http\://sockshare\.ac/themes/movies/img/icon/server/(.+?)\.png" width="16" height="16" /> <a href="(.+?)">Version ').findall(r)
				for host, url in match:
					if host == 'internet':
						pass
					else:
						sources.append({
							'source': host,
							'quality': 'SD',
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
		r = client.request(url)
		match = re.compile('Base64\.decode\("(.+?)"').findall(r)
		for iframe in match:
			iframe = base64.b64decode(iframe)
			match = re.compile('src="(.+?)"').findall(iframe)
			for url in match:
				return url