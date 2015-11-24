#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
import json
from base import BaseFeedBook
from lib.url_req import URLOpener
from bs4 import BeautifulSoup
import re

def getBook():
	return Shuwu

class Shuwu(BaseFeedBook):
	title                 = u'书屋'
	description           = u'动态更新'
	network_timeout = 60
	language = 'zh-cn'
	feed_encoding = "GB2312"
	#page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	fulltext_by_readability = False
	fulltext_by_instapaper = False
	keep_only_tags = [dict(name='p')]
	remove_tags = ['input','textarea']
	remove_ids = []
	remove_classes = ['MsoPlainText']
	remove_attrs = []

	feeds = [
          (u'书屋', 'http://www.housebook.com.cn/old.htm'),
              ]


	def ParseFeedUrls(self):
		urls = []
		urladded = set()
		url = self.feeds[0][1]
		section = self.feeds[0][0]
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		if result.code == 200 and result.content:
			content = result.content.decode(self.feed_encoding)
			soup = BeautifulSoup(content, "lxml")
			tag_a = soup.find_all('a')
			href = tag_a[1]['href']
			temp_url = href[0:6]
			url = 'http://www.housebook.com.cn/'+ href
			result = opener.open(url)
			if result.code != 200:
				self.log.warn('fetch rss failed:%s'%mainurl)
				return []
			content = result.content.decode(self.feed_encoding)
			soup = BeautifulSoup(content, "lxml")
			tag_a = soup.find_all('a')
			for art in tag_a:
				if art['href'] == '../main.htm':
					continue
				urlfeed = 'http://www.housebook.com.cn/' + temp_url +'/' +art['href']
				title = art.text
				urls.append((section, title, urlfeed, None))
				urladded.add(urlfeed)
		else:
			self.log.warn('fetch rss failed(%d):%s'%(result.code,url))
		return urls

	def fetcharticle_1(self, url, decoder):
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		status_code, content = result.code, result.content
		if status_code != 200 or not content:
			self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
			return None

		if self.page_encoding:
			return content.decode(self.page_encoding)
		else:
			return decoder.decode(content,url)
