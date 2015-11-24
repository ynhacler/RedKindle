#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
import json
from base import BaseFeedBook
from lib.url_req import URLOpener
from bs4 import BeautifulSoup, Comment,NavigableString,CData,Tag

def getBook():
	return Lianhe_china

class Lianhe_china(BaseFeedBook):
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
          (u'联合早报', 'http://zaobao.feedsportal.com/c/34003/f/616930/index.rss'),
              ]

	http_daili = 'http://go2.10086.cn/%s'

	def ParseFeedUrls(self):
		urls = []
		urladded = set()
		url = self.feeds[0][1]
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		section = self.feeds[0][0]
		if result.code == 200 and result.content:
			soup = BeautifulSoup(result.content,'lxml')
			cont1 = soup.findAll("title")
			cont2 = soup.findAll("guid")
			nums = len(cont2)
			for i in range(nums):
				title = cont1[i+2].string
				href = cont2[i].string
				url = self.trueURL_zzh(href)
				urls.append((section, title, url, None))
		else:
			self.log.warn('fetch rss failed(%d):%s'%(result.code,url))
		return urls


	def trueURL_zzh(self,urls):
		count = 0
		temp_i = 0
		for c in urls:
			temp_i += 1
			if c == '/':
				count += 1
			if count == 3:
				break
		newurl = urls[0:temp_i]+'print/'+urls[temp_i:]
		return newurl


	def fetcharticle2(self, url, decoder):
		#url = self.http_daili % url[7:]
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		print result.realurl
		status_code, content = result.code, result.content
		if status_code != 200 or not content:
			self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
			return None
		soup = BeautifulSoup(content,'lxml')
		cont = soup.findAll(attrs={"align":"right"})
		url = cont[0].a['href']

		url = self.trueURL_zzh(url)
		#文章url
		result = opener.open(url)
		status_code, content = result.code, result.content
		if status_code != 200 or not content:
			self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
			return None

		if self.page_encoding:
			return content.decode(self.page_encoding)
		else:
			return decoder.decode(content,url)
