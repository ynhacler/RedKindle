# -*- coding:utf-8 -*-

import urllib, urllib2, Cookie, urlparse,time
from config import *
import gzip
import StringIO

class SmartHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
	__cookie_flag = 'Set-Cookie: '

	@staticmethod
	def __find_cookie(headers):
		for msg in headers:
			if msg.find(SmartHTTPRedirectHandler.__cookie_flag) != -1:
				return msg.replace(SmartHTTPRedirectHandler.__cookie_flag, '')
                return ''

	def http_error_301(self, req, fp, code, msg, httpmsg):
		cookie = SmartHTTPRedirectHandler.__find_cookie(httpmsg.headers)
		if cookie != '':
			req.add_header("Cookie", cookie)
		return urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, httpmsg)

	def http_error_302(self, req, fp, code, msg, httpmsg):
		cookie = SmartHTTPRedirectHandler.__find_cookie(httpmsg.headers)
		if cookie != '':
			req.add_header("Cookie", cookie)
		return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, httpmsg)


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
			headers={}

		response = resp()

		cnt = 0
		while cnt < self.maxFetchCount:
			try:
				req = urllib2.Request(url,data,self._getHeaders(url))
				opener = urllib2.build_opener(SmartHTTPRedirectHandler)
				response = opener.open(req,timeout=self.timeout)
				response.content = response.read()
				# 处理gzip过的页面
				if response.headers.get('content-encoding', None) == 'gzip':
					response.content = gzip.GzipFile(fileobj=StringIO.StringIO(response.content)).read()
				response.realurl = response.geturl()
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
	print test.geturl()
	print test.code
	print test.content
	print test.headers
