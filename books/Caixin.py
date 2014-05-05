#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib,datetime
from bs4 import BeautifulSoup, Comment,NavigableString,CData,Tag
from base import BaseFeedBook
from lib.url_req import URLOpener
from lib import feedparser
from lib.readability import readability
from lib.img import rescale_image


def getBook():
	return Caixin

class Caixin(BaseFeedBook):
	title = u'财新网'
	network_timeout = 60
	language = 'zh-cn'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	mastheadfile = "mh_zhihudaily.gif"
	coverfile = "cv_zhihudaily.jpg"
	remove_tags = []
	remove_ids = []
	remove_classes = []
	remove_attrs = []

	feeds = [
	(u'财新网','http://magazine.caixin.com/comparative_studies/rss/100206855.xml'),
	]

	def ParseFeedUrls(self):
                #解析xml，返回相关信息
                """ return list like [(section,title,url,desc),..] """
                urls = []
                tnow = datetime.datetime.utcnow()
                urladded = set()

                for feed in self.feeds:
                        section,url = feed[0],feed[1]
                        isfulltext = feed[2] if len(feed)>2 else False
                        timeout = self.timeout+10 if isfulltext else self.timeout
                        opener = URLOpener(self.host,timeout=timeout)
                        result = opener.open(url)

                        if result.code == 200 and result.content:
                                if self.feed_encoding:
                                        content = result.content.decode(self.feed_encoding)
                                else:
                                        content = AutoDecoder(True).decode(result.content,url)
                                feed = feedparser.parse(content)#进行解析

                                #分解得到的内容
                                for e in feed['entries'][:self.max_articles_per_feed]:#取相应数量的feed
                                        #支持HTTPS
                                        urlfeed = e.link.replace('http://','https://') if url.startswith('https://') else e.link
					testurl = urlfeed[0:len(urlfeed)-5]+'_all.html'
                                        if urlfeed in urladded:
                                                continue

                                        desc = None
                                        if isfulltext:
                                                if hasattr(e,'content') and e.content[0]['value']:
                                                        desc = e.content[0]['value']
                                                elif hasattr(e,'description'):
                                                        desc = e.description
                                                else:
                                                        self.log.warn('fulltext feed item no has desc,link to webpage for article.(%s)' % e.title)
                                        urls.append((section, e.title, urlfeed, desc))
                                        urladded.add(urlfeed)
                        else:
                                self.log.warn('fetch rss failed(%d):%s'%(result.code,url))

                return urls

