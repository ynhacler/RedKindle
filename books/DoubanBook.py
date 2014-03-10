#!//usr/bin/env python
# -*- coding:utf-8 -*-


import urllib
from base import BaseFeedBook
from lib.url_req import URLOpener

def getBook():
	return DoubanBook

class DoubanBook(BaseFeedBook):
	title = u'豆瓣最受欢迎的书评'
	description = u'豆瓣成员投票选出的最佳书评'
	network_timeout = 60
	oldest_article        = 40
	language = 'zh-cn'
	feed_encoding = "utf-8"
	page_encoding = "utf-8"
	fulltext_by_readability = False
	fulltext_by_instapaper = False
	keep_only_tags = [dict(name='h1'),dict(name='div', attrs={'class':'piir'})]
	remove_tags = []
	remove_ids = ['db-global-nav','db-nav-book']
	remove_classes = ['pil ','review-stat','rec-sec','report-lnk']
	remove_attrs = []
	feeds = [
	(u'豆瓣书评', 'http://book.douban.com/feed/review/book'),
	]

