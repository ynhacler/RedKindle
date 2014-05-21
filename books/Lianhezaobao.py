#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
import json
from base import BaseFeedBook
from lib.url_req import URLOpener
from bs4 import BeautifulSoup, Comment,NavigableString,CData,Tag

def getBook():
	return Lianhezaobao

class Lianhezaobao(BaseFeedBook):
	title                 = u'联合早报'
	description           = u'动态更新'
	network_timeout = 60
	language = 'zh-cn'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	keep_only_tags = []
	remove_tags = []
	remove_ids = []
	remove_classes = []
	remove_attrs = []
	feeds = [
          (u'联合早报', 'http://zaobao.feedsportal.com/c/34003/f/616929/index.rss'),
              ]


	def fetcharticle2(self, url, decoder):
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		status_code, content = result.code, result.content

		print content
		if status_code != 200 or not content:
			self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
			return None
		soup = BeautifulSoup(content,'lxml')
		cont = soup.findAll(attrs={"align":"right"})
		print cont
		url = cont[0].a['href']

		result = opener.open(url)
		status_code, content = result.code, result.content
		if status_code != 200 or not content:
			self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
			return None

		if self.page_encoding:
			return content.decode(self.page_encoding)
		else:
			return decoder.decode(content,url)
