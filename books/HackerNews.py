#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
from bs4 import BeautifulSoup, Comment,NavigableString,CData,Tag
from base import BaseFeedBook
from lib.url_req import URLOpener

def getBook():
	return HackerNews

class HackerNews(BaseFeedBook):
	title = u'HackerNews'
	network_timeout = 60
	language = 'en'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	fulltext_by_instapaper = False
	#keep_only_tags = [dict(name='div', attrs={'class':'page-content'})]
	remove_tags = []
	remove_ids = []
	remove_classes = []
	remove_attrs = []

	feeds = [
	('HackerNews','https://news.ycombinator.com/rss'),
	]

	def ParseFeedUrls(self):
		urls = []
		urladded = set()
		url = self.feeds[0][1]
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		section = self.feeds[0][0]
		if result.code == 200 and result.content:
			soup = BeautifulSoup(result.content,'lxml')
			cont = soup.findAll('item')
			for con in cont:
				title = con.title.get_text()
				href = con.contents[2]
				urls.append((section, title, href, None))
		else:
			self.log.warn('fetch rss failed(%d):%s'%(result.code,url))
		return urls



