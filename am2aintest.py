# -*- coding:utf-8 -*-
import os,re,urllib,urlparse,datetime,logging
from datetime import date, timedelta
from config import *
from books.base import BaseFeedBook,  BaseUrlBook,WebpageBook
from jinja2 import Environment, PackageLoader
from os import path, listdir, system
from shutil import copy,copytree

from books.ZhihuDaily import ZhihuDaily
from books.DoubanBook import DoubanBook

def render_and_write(template_name, context, output_name, output_dir):
	"""Render `template_name` with `context` and write the result in the file
	`output_dir`/`output_name`."""

        template = templates_env.get_template(template_name)
        f = open(path.join(output_dir, output_name), "w")
        f.write(template.render(**context).encode('utf-8'))
        f.close()

def mobi(input_file, exec_path):
	system("%s %s" % (exec_path, input_file))




log = logging.getLogger()

feeds=[[u'163easynet',"http://www.xinhuanet.com/ent/news_ent.xml"],
[u'XXXzzhXXX',"http://www.sciencenet.cn/xml/news.aspx?news=0"]]
feeds2=[[u'XXXzzhXXX',"http://www.sciencenet.cn/xml/news.aspx?news=0"]]
feeds3=[[u'163easynet',"http://www.xinhuanet.com/ent/news_ent.xml"]]
feeds4=[[u'3lian','http://feed.36kr.com/c/33346/f/566026/index.rss']]
feeds5=[[u'nytimes','http://cn.nytimes.com/rss.html',True]]

zzh = BaseFeedBook(log)
zzh2 = ZhihuDaily(log)
#zzh2 = DoubanBook(log)
zzh.feeds = feeds5
zzh.keep_image = False
zzh2.keep_image = False
#zzh.fulltext_by_readability = False
#zzh.fulltext_by_instapaper = False

zzhs = []
#zzhs.append(zzh)
zzhs.append(zzh2)
#总的img计数
imgindex_temp = 0

#所有的信息
data = []
feed_number = 1
entry_number = 0
play_order = 0

temp_sec = ''

#输出目录
output_dir='/home/zzh/Desktop/temp/v3'

ROOT = path.dirname(path.abspath(__file__))

templates_env = Environment(loader=PackageLoader('amaintest', 'templates2'))


if __name__ == '__main__':
	img_num = []

	i=-1 #对feed进行计数

	#自动处理的
	for zz in zzhs:
		zz._imgindex = imgindex_temp
		for sec_or_media, url, title, content,brief in zz.Items():
			if sec_or_media.startswith(r'image/'):
				filename = 'image/'+title
				img_num.append(title)
				fout = open(filename, "wb")
				fout.write(content)
				fout.close()
			else:
				#新的feed开始
				if temp_sec != sec_or_media:
					temp_sec = sec_or_media
					feed_number += 1
					play_order += 1
					entry_number = 0
					local = {
						'number':feed_number,
						'play_order':play_order,
						'entries':[],
						'title':sec_or_media
					}
					i += 1
					data.insert(i,local)
				#处理文章
				play_order += 1
				entry_number += 1

				local_entry = {
					'number':entry_number,
					'play_order':play_order,
					'title':title,
					'description':brief,
					'content':content,
					'url':url,
				}

				data[i]['entries'].append(local_entry)
		#raw_input("Input your id plz")
		imgindex_temp = zz._imgindex
		#======================end for
	#手动处理的
	'''
			filename = 'image/doc/'+str(play_order)+'.html'
			fout = open(filename, "wb+")
			fout.write(content.encode('utf-8'))
			fout.close()
	'''

	wrap ={
		'date': date.today().isoformat(),
		'feeds':data,
		'img_nums':imgindex_temp,
		'img_name':img_num,
	}

	## TOC (NCX)
	render_and_write('toc.xml', wrap, 'toc.ncx', output_dir)
	## COVER (HTML)
	render_and_write('cover.html',wrap,'cover.html',output_dir)
	## TOC (HTML)
	render_and_write('toc.html', wrap, 'toc.html', output_dir)
	## OPF
	render_and_write('opf.xml', wrap, 'daily.opf', output_dir)
	#/home/zzh/Desktop/temp/v3
	for feed in data:
		for entry in feed['entries']:
			render_and_write('feed.html',entry,'article_%s_%s.html' % (feed['number'],entry['number']),output_dir)

	for name in listdir(path.join(ROOT, 'image')):
		copy(path.join(ROOT, 'image', name), path.join(output_dir, name))

	copy(path.join(ROOT, 'templates2', 'masthead.jpg'), path.join(output_dir, 'masthead.jpg'))
	copy(path.join(ROOT, 'templates2', 'cover.jpg'), path.join(output_dir, 'cover.jpg'))

	mobi(path.join(output_dir,'daily.opf'),path.join(ROOT,'kindlegen_1.1'))
	#copytree(path.join(ROOT, 'image'), path.join(output_dir,'image'))
	print zzh._imgindex
	print '-=end=-'

