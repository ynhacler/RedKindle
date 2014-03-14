#-*- coding:utf-8 -*-

import os,re,urllib,urlparse,datetime,logging
from datetime import date, timedelta
from books.base import BaseFeedBook,  BaseUrlBook,WebpageBook
from jinja2 import Environment, PackageLoader
from os import path, listdir, system
from shutil import copy,copytree,rmtree
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base  import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import mimetypes
from random import randrange
import model
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

#动态载入手工处理的feeds
from books import FeedClasses, FeedClass

from config import *


#生产模板
def render_and_write(template_name, context, output_name, output_dir,templates_env):
	"""Render `template_name` with `context` and write the result in the file
	`output_dir`/`output_name`."""
	template = templates_env.get_template(template_name)
	f = open(path.join(output_dir, output_name), "w")
	f.write(template.render(**context).encode('utf-8'))
	f.close()

#生产mobi
def mobi(input_file, exec_path,logging=None):
	"""Execute the KindleGen binary to create a MOBI file."""
	try:
		logging.info("generate .mobi file start... ")
		system("%s %s" % (exec_path, input_file))
		return 'metadata.mobi'
	except Exception, e:
		logging.error("Error: %s" % e)
		return ''

#epub
def epub(r_path,t_path,e_path, logging=None):
	try:
		os.chdir(path.join(r_path,t_path,e_path))

		logging.info("generate .epub file start... ")
		system("zip -X -9 -r book1.epub.zip * -x mimetype")
		system("zip -X -0 book1.epub.zip mimetype")
		system("mv book1.epub.zip daily.epub")

		os.chdir(r_path)
		return 'daily.epub'
	except Exception, e:
		logging.error("Error: %s" % e)
		return ''

#发邮件
def send_mail(from_addr,to_addr,attach_path,ifmobi,logging=None):
	try:
		msg = MIMEMultipart()
		msg['From'] = from_addr
		msg['To'] = to_addr
		msg['Subject'] = 'Redkindle'
		msg.attach(MIMEText(''))
		ctype, encoding = mimetypes.guess_type(attach_path)
		if ctype is None or encoding is not None:
			ctype = 'application/octet-stream'
		maintype, subtype = ctype.split('/', 1)
		part = MIMEBase(maintype, subtype)
		with open(attach_path, 'rb') as fp:
			part.set_payload(fp.read())
		encoders.encode_base64(part)
		if ifmobi == 1:
			filename=ATTACH_FILENAME+".mobi"
		else:
			filename=ATTACH_FILENAME+".epub"
		part.add_header('Content-Disposition', 'attachment', filename=filename)
		msg.attach(part)
		smtp = smtplib.SMTP('127.0.0.1', 25)
		smtp.sendmail(from_addr, to_addr, msg.as_string())
		smtp.quit()
	except Exception, e:
		logging.error("fail:%s" % e)


#抓文章存在mysql
def pushwork2(f_id,feeds):
	#区别是自动还是手动处理的
	log = logging.getLogger()

	#自动
	if cmp('http',feeds[0][1][0:4].lower()) == 0:
		redbook = BaseFeedBook(log)
		redbook.feeds = feeds
	else:
		#手动
		mfeedclasses = FeedClasses()
		for mfeed in mfeedclasses:
			for my_mfeed in feeds:
				if mfeed.__name__ == my_mfeed[1]:
					redbook = mfeed(log)

	ROOT = path.dirname(path.abspath(__file__))
	temp_dir = path.join(ROOT, 'temp')
	#创建文件夹
	output_dir = path.join(temp_dir,'feed_%s' % f_id)
	isExists = path.exists(output_dir)
	if isExists:
		rmtree(output_dir)
		time.sleep(3)

	isExists = path.exists(output_dir)
	if not isExists:
		os.makedirs(output_dir)
		print 'mkdir'
		time.sleep(1)

	#清空对应的mysql表
	model.delete_old_article(f_id)
	time.sleep(0.5)

	for sec_or_media, url, title, content,brief in redbook.Items():
		if sec_or_media.startswith(r'image/'):
			filename = path.join(output_dir,title)
			fout = open(filename, "wb")
			fout.write(content)
			fout.close()
		else:
			model.put_section_article(f_id,sec_or_media, url, title, content,brief)

	#改变更新时间
	model.update_article_update_time(f_id)
	print '-=end grasp=-'



#worker生产电子书，并推送
def pushwork(email,feeds,mfeeds,ifimg):
#	log = default_log
	log = logging.getLogger()

	#放所有的feeds（手工和自动处理的）
	feedsclasses = []
	#得到出手工处理的feed目录
	mfeedclasses = FeedClasses()
	for mfeed in mfeedclasses:
		for my_mfeed in mfeeds:
			print mfeed.__name__
			print my_mfeed[0]
			print '-=-=-=-=-=-=-=-'
			if mfeed.__name__ == my_mfeed[0]:
				temp_mfeed = mfeed(log)
				feedsclasses.append(temp_mfeed)

	#自动处理的
	redbook = BaseFeedBook(log)
	redbook.feeds = feeds
	feedsclasses.append(redbook)

	#是否要图片
	if ifimg == 0:
		for feed in feedsclasses:
			feed.keep_image = False

	#所有的信息
	sum_pic_size = 0#getsize('test.png')/1024 MAX_PIC_SIZE
	data = []
	feed_number = 1
	entry_number = 0
	play_order = 0
	#总的img计数
	imgindex_temp = 0

	temp_sec = ''

	ROOT = path.dirname(path.abspath(__file__))
	output_dir = path.join(ROOT, 'temp')

	templates_env = Environment(loader=PackageLoader('bmaintest', 'templates2'))

	img_num = []

	i=-1 #对feed进行计数

	for feed in feedsclasses:
		print feed.__class__.__name__
		print '--------'
		feed._imgindex = imgindex_temp
		for sec_or_media, url, title, content,brief in feed.Items():
			if sec_or_media.startswith(r'image/'):
					if sum_pic_size < MAX_PIC_SIZE:
						filename = path.join(ROOT, 'temp',title)
						img_num.append(title)
						fout = open(filename, "wb")
						fout.write(content)
						fout.close()
						sum_pic_size += path.getsize(filename)/1024

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
		imgindex_temp = feed._imgindex

	#=====================end for

	wrap ={
		'date': date.today().isoformat(),
		'feeds':data,
		'img_nums':imgindex_temp,
		'img_name':img_num,
	}

	## TOC (NCX)
	render_and_write('toc.xml', wrap, 'toc.ncx', output_dir,templates_env)
	## COVER (HTML)
	render_and_write('cover.html',wrap,'cover.html',output_dir,templates_env)
	## TOC (HTML)
	render_and_write('toc.html', wrap, 'toc.html', output_dir,templates_env)
	## OPF
	render_and_write('opf.xml', wrap, 'daily.opf', output_dir,templates_env)
	#/home/zzh/Desktop/temp/v3
	for feed in data:
		for entry in feed['entries']:
			render_and_write('feed.html',entry,'article_%s_%s.html' % (feed['number'],entry['number']),output_dir,templates_env)

	#copy cover.jpg
	copy(path.join(ROOT, 'templates2', 'masthead.jpg'), path.join(output_dir, 'masthead.jpg'))
	copy(path.join(ROOT, 'templates2', 'cover.jpg'), path.join(output_dir, 'cover.jpg'))


	#gen mobi
	mobi_file = mobi(path.join(output_dir,'daily.opf'),path.join(ROOT,'kindlegen_1.1') ,log)

	#send mail
	if mobi_file :
		mobi_file = path.join(output_dir,mobi_file)
#fp = open(mobi_file, 'rb')
#		sendmail(fp.read())
#		fp.close()
		send_mail(SrcEmail,email,mobi_file,log)

	#clean
	for fn in listdir(output_dir):
		f_path = path.join(output_dir, fn)
		if path.isfile( f_path):
			os.remove(f_path)

	return '-=end=-'


#从mysql中提取数据
def pushwork3(email,feeds,ifimg,ifmobi):#feeds只存有编号,ifmobi=1
	#相关信息
	log = logging.getLogger()
	sum_pic_size = 0#getsize('test.png')/1024 MAX_PIC_SIZE
	data = []
	feed_number = 1
	entry_number = 0
	play_order = 0
	#总的img计数
	imgindex_temp = 0
	temp_sec = ''

	ROOT = path.dirname(path.abspath(__file__))
	if ifmobi == 1:
		output_dir = path.join(ROOT, 'temp','mobi')
	else:
		output_dir = path.join(ROOT, 'temp','epub','OEBPS')

	templates_env = Environment(loader=PackageLoader('bmaintest', 'templates2'))

	img_num = []

	i=-1 #对feed进行计数

	for feed in feeds:
		#从mysql中读取
		temp_article = model.get_article2id(feed)
		if len(temp_article) == 0:
			continue

		feed_number +=1
		play_order += 1
		entry_number = 0
		local = {
			'number':feed_number,
			'play_order':play_order,
			'entries':[],
			'title':''
		}
		i += 1
		data.insert(i,local)
		for article in temp_article:
			play_order += 1
			entry_number += 1
			local_entry = {
				'number':entry_number,
				'play_order':play_order,
				'title':article['title'],
				'description':article['brief'],
				'content':article['content'],
				'url':article['url'],
			}
			data[i]['entries'].append(local_entry)
			data[i]['title'] = article['section']
		#图片
		if ifimg == 1:
			img_dir = path.join(ROOT,'temp','feed_%s' % feed)
			for fn in listdir(img_dir):
				if sum_pic_size < MAX_PIC_SIZE:
					f_path = path.join(img_dir, fn)
					sum_pic_size += path.getsize(f_path)/1024
					img_num.append(fn)
					copy(f_path, path.join(output_dir, fn))
					imgindex_temp += 1
		else:
			imgindex_temp = 0
			img_num = []



	#==============================end for

	wrap ={
		'date': date.today().isoformat(),
		'feeds':data,
		'img_nums':imgindex_temp,
		'img_name':img_num,
	}

	## TOC (NCX)
        render_and_write('toc.xml', wrap, 'toc.ncx', output_dir,templates_env)
	## COVER (HTML)
	render_and_write('cover.html',wrap,'cover.html',output_dir,templates_env)
	## TOC (HTML)
	render_and_write('toc.html', wrap, 'toc.html', output_dir,templates_env)
	## OPF
	render_and_write('opf.xml', wrap, 'metadata.opf', output_dir,templates_env)
	#/home/zzh/Desktop/temp/v3
	for feed in data:
		for entry in feed['entries']:
			render_and_write('feed.html',entry,'article_%s_%s.html' % (feed['number'],entry['number']),output_dir,templates_env)

	#copy cover.jpg
	copy(path.join(ROOT, 'templates2', 'masthead.jpg'), path.join(output_dir, 'masthead.jpg'))
	copy(path.join(ROOT, 'templates2', 'cover.jpg'), path.join(output_dir, 'cover.jpg'))


	#gen mobi
	if ifmobi == 1:
		mobi_file = mobi(path.join(output_dir,'metadata.opf'),path.join(ROOT,'kindlegen_1.1') ,log)

		if mobi_file :
			mobi_file = path.join(output_dir,mobi_file)
			send_mail(SrcEmail,email,mobi_file,1,log)
	else:
		epub_file = epub(ROOT,'temp','epub',log)

		if epub_file:
			epub_file = path.join(ROOT,'temp','epub',epub_file)
			send_mail(SrcEmail,email,epub_file,0,log)
			if path.isfile( epub_file):
				os.remove(epub_file)

	#clean
	for fn in listdir(output_dir):
		f_path = path.join(output_dir, fn)
		if path.isfile( f_path):
			os.remove(f_path)

	return '-=end=-'

if __name__=="__main__":
	pushwork3('aaaa',[16],0,1)
