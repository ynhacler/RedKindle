#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

_feedsclasses = []
def RegisterFeed(feed):
	if feed.title:
		_feedsclasses.append(feed)

def FeedClasses():
	return _feedsclasses

def FeedClass(title):
	for bk in _feedsclasses:
		if bk.title == title:
			return bk
	return None

#LoadFeeds
for bkfile in os.listdir(os.path.dirname(__file__)):
	if bkfile.endswith('.py') and not bkfile.startswith('__') and not bkfile.endswith("base.py"):
		bookname = os.path.splitext(bkfile)[0]
		try:
			mbook = __import__("books." + bookname, fromlist='*')
			bk = mbook.getBook()
			RegisterFeed(bk)
		except Exception as e:
			default_log.warn("Feed '%s' import failed : %s" % (bookname,e))
