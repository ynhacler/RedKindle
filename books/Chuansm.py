#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
from bs4 import BeautifulSoup, Comment,NavigableString,CData,Tag
from base import BaseFeedBook
from lib.url_req import URLOpener

def getBook():
	return Chuansm 

class Chuansm(BaseFeedBook):
	title = u'传送门'
	network_timeout = 60
	language = 'zh-cn'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	fulltext_by_readability = False
	fulltext_by_instapaper = False
	keep_only_tags = [dict(name='div', attrs={'class':'page-content'})]
	remove_tags = []
	remove_ids = []
	remove_classes = []
	remove_attrs = []

	feeds = [
	(u'传送门','http://chuansong.me/'),
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
			cont = soup.findAll(attrs={"class":"feed_item_question"})
			for con in cont:
				title = con.a.get_text()
				href = "http://chuansongme.com%s" % con.a['href']
				urls.append((section, title, href, None))
		else:
			self.log.warn('fetch rss failed(%d):%s'%(result.code,url))
		return urls



