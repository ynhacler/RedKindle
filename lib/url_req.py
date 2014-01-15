# -*- coding:utf-8 -*-

import Cookie, urlparse,time
import requests

from config import *

class URLOpener:
	def __init__(self, host=None, maxfetchcount=2, maxredirect=3, timeout=CONNECTION_TIMEOUT, addreferer=False):
		self.cookie = Cookie.SimpleCookie()
		self.maxFetchCount = maxfetchcount
		self.maxRedirect = maxredirect
		self.host = host
		self.addReferer = addreferer
		self.timeout = timeout

	def open(self, url, data=None):
		self.realurl = url
		maxRedirect = self.maxRedirect

		class resp:
			code=555
			content=None
			url = ''
			headers={}

		response = resp()

		cnt = 0
		while cnt < self.maxFetchCount:
			try:
#				req = urllib2.Request(url,data,self._getHeaders(url))
#				opener = urllib2.build_opener(SmartHTTPRedirectHandler)
#				response = opener.open(req,timeout=self.timeout)
				s = requests.Session()
				req = s.get(url,data=data,headers=self._getHeaders(url),allow_redirects=True,timeout=self.timeout)
				self.realurl = req.url
				response.content = req.content
				response.code = req.status_code
				response.headers = req.headers
				response.realurl = req.url
			except:
				cnt += 1
				time.sleep(1)
			else:
				break

		return response



	def _getHeaders(self, url=None):
		headers = {
				'User-Agent':"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		}
		cookie = '; '.join(["%s=%s" % (v.key, v.value) for v in self.cookie.values()])
		if cookie:
			headers['Cookie'] = cookie
		if self.addReferer and (self.host or url):
			headers['Referer'] = self.host if self.host else url
		return headers




if __name__ == "__main__":
#	test = URLOpener().open('http://www.11seba.com/')
#	test = URLOpener().open('http://video.sina.com.cn/news/')
#	test = URLOpener().open('http://www.facebook.com')
	test = URLOpener().open('http://t.cn/8ks1UQM')
	print test.url
	print test.code
	print isinstance(test.content,unicode)
	print test.headers
	print test.content
