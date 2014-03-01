import os, re, urllib, urlparse, imghdr, logging, datetime
from urllib2 import *
import chardet
import gzip
import StringIO
import redis

from bs4 import BeautifulSoup, Comment, NavigableString, CData, Tag
from lib import feedparser
from lib.readability import readability
from lib.url_req import URLOpener

#url = "http://www.baidu.com/"
'''
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
url="http://blog.sina.com.cn/u/1657875817"

content = urlopen(url).read()
encoding = chardet.detect(content)['encoding']
print encoding
result = content.decode(encoding)

netloc = urlparse.urlsplit(url)[1]

print netloc
r.set(netloc,encoding)

print r.get(netloc)
'''
#url='http://tech.sina.com.cn/internet/'
#url='http://tech.sina.com.cn/i/2014-01-08/08039077686.shtml'
#url='http://blog.knownsec.com/2012/04/about-content-encoding-gzip/'
url ='http://book.douban.com/review/6549990/'
zzh=URLOpener()
re=zzh.open(url)
#print re.info()
#print re.content.decode('GBK').encode('utf-8')
#print re.content
fout=open('zhang_test','wb')
fout.write(re.content)
fout.close()
'''
encoding = chardet.detect(re.content)['encoding']
print encoding
print re.headers
print isinstance(re.content,unicode)
print re.content.decode(encoding,'ignore').encode('utf-8')
'''
doc = readability.Document(re.content)
summary = doc.summary(html_partial=True)
soup = BeautifulSoup(re.content,'lxml')
print soup.body.contents[0]
