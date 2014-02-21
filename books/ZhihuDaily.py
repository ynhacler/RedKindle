#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
import json
from base import BaseFeedBook
from lib.url_req import URLOpener

def getBook():
	return ZhihuDaily

class ZhihuDaily(BaseFeedBook):
	title                 = u'知乎日报'
	description           = u'知乎日报内容动态更新'
	network_timeout = 60
	language = 'zh-cn'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	fulltext_by_readability = False
	fulltext_by_instapaper = False
	keep_only_tags = [dict(name='h1', attrs={'class':'headline-title'}),
	dict(name='div', attrs={'class':'question'})]
	remove_tags = []
	remove_ids = []
	remove_classes = ['view-more', 'avatar']
	remove_attrs = []
	extra_css = """
	.question-title {font-size:1.1em;font-weight:normal;text-decoration:underline;color:#606060;}
	.meta {font-size:0.9em;color:#808080;}
	"""
	feeds = [
          (u'今日头条', 'http://news.at.zhihu.com/api/1.2/news/latest'),
              ]

	partitions = [('top_stories',u'今日头条'),('news',u'今日热闻'),]

	def ParseFeedUrls(self):
		urls = []
		urladded = set()
		url = self.feeds[0][1]
		opener = URLOpener(self.host, timeout=self.timeout)
		result = opener.open(url)
		if result.code == 200 and result.content:
			feed = json.loads(result.content.decode(self.feed_encoding))

			for partition,section in self.partitions:
				for item in feed[partition]:
					urlfeed = item['share_url']
					if urlfeed in urladded:
						self.log.info('skipped %s' % urlfeed)
						continue
					urls.append((section, item['title'], urlfeed, None))
					urladded.add(urlfeed)
		else:
			self.log.warn('fetch rss failed(%d):%s'%(result.code,url))
		return urls

	def fetcharticle(self, url, decoder):
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
