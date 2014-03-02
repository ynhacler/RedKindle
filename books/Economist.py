#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook,  string_of_tag
from lib.url_req import URLOpener
import re

def getBook():
    return Economist

class Economist(BaseFeedBook):
	title                 = 'The Economist'
	description           = 'Global news and current affairs from a European perspective. deliver on Friday.'
	language              = 'en'
	feed_encoding         = "utf-8"
	page_encoding         = "utf-8"
	mastheadfile          = "mh_economist.gif"
	coverfile             = "cv_economist.jpg"
#    deliver_days          = ['Friday',]
    	
	remove_classes = ['ec-messages',]
    
	feeds = [
	            ('Index', 'http://www.economist.com/printedition'),
	]
    
	def ParseFeedUrls(self):
		""" return list like [(section,title,url,desc),..] """
	        mainurl = 'http://www.economist.com/printedition'
	        urls = []
	        urladded = set()
	        opener = URLOpener(self.host, timeout=30)
	        result = opener.open(mainurl)
	        if result.code != 200:
	            self.log.warn('fetch rss failed:%s'%mainurl)
	            return []
	     
	        content = result.content.decode(self.feed_encoding)
	        soup = BeautifulSoup(content, "lxml")
#href=re.compile("elsie") 
		for section in soup.find_all(id=re.compile("section-")):
			h4 = section.find('h4')
			if h4 is None:
				self.log.warn('h4 is empty')
				continue
			sectitle = string_of_tag(h4).strip()
			if not sectitle:
				self.log.warn('h4 string is empty')
				continue
			#self.log.info('Found section: %s' % section_title)
			articles = []
			subsection = ''
			for node in section.find_all(class_='article'):
				subsec = node.find('h5')
				if subsec is not None:
					subsection = string_of_tag(subsec)
				prefix = (subsection + ': ') if subsection else ''
				a = node.find('a', attrs={"href":True}, recursive=False)
				if a is not None:
					url = a['href']
					if url.startswith(r'/'):
						url = 'http://www.economist.com' + url
					url += '/print'
					title = string_of_tag(a)
					if title:
						title = prefix + title
						#self.log.info('\tFound article:%s' % title)
						if url not in urladded:
							urls.append((sectitle,title,url,None))
							urladded.add(url)
		if len(urls) == 0:
			self.log.warn('len of urls is zero.')
		return urls
