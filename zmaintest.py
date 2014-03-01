import os,re,urllib,urlparse,datetime,logging
from config import *
from books.base import BaseFeedBook,  BaseUrlBook,WebpageBook

log = logging.getLogger()

feeds=[[u'163easynet',"http://www.xinhuanet.com/ent/news_ent.xml"],
[u'XXXzzhXXX',"http://www.sciencenet.cn/xml/news.aspx?news=0"]]

feeds1=[[u'=-=-=asff','http://tech.sina.com.cn/i/2014-01-08/08039077686.shtml']]
#feeds2=[['324','http://blog.csdn.net/b2b160/article/details/4030702']]
zzh = BaseFeedBook(log,2)
zzh.feeds = feeds

i=0
for sec_or_media, url, title, content,brief in zzh.Items():
	if sec_or_media.startswith(r'image/'):
		filename = 'image/'+title
		fout = open(filename, "wb")
		fout.write(content)
		fout.close()
	else:
		i += 1
		filename = 'image/'+str(i)+'.html'
		fout = open(filename, "wb+")
		fout.write(content.encode('utf-8'))
		fout.close()

