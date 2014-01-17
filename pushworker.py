#-*- coding:utf-8 -*-

import os,re,urllib,urlparse,datetime,logging
from datetime import date, timedelta
from books.base import BaseFeedBook,  BaseUrlBook,WebpageBook
from jinja2 import Environment, PackageLoader
from os import path, listdir, system
from shutil import copy,copytree
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base  import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import mimetypes
from random import randrange

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
		return 'daily.mobi'
	except Exception, e:
		logging.error("Error: %s" % e)
		return ''

#发邮件
def send_mail(from_addr,to_addr,attach_path,logging=None):
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
		part.add_header('Content-Disposition', 'attachment', filename=ATTACH_FILENAME)
		msg.attach(part)
		smtp = smtplib.SMTP('127.0.0.1', 25)
		smtp.sendmail(from_addr, to_addr, msg.as_string())
		smtp.quit()
	except Exception, e:
		logging.error("fail:%s" % e)
#test
def pushwork2(a,b):
	ROOT = path.dirname(path.abspath(__file__))
	return ROOT


#worker生产电子书，并推送
def pushwork(email,feeds):
#	log = default_log
	log = logging.getLogger()

	redbook = BaseFeedBook(log)
	redbook.feeds = feeds

	#所有的信息
	data = []
	feed_number = 1
	entry_number = 0
	play_order = 1

	temp_sec = ''

	ROOT = path.dirname(path.abspath(__file__))
	output_dir = path.join(ROOT, 'temp')

	templates_env = Environment(loader=PackageLoader('bmaintest', 'templates'))

	img_num = []

	i=-1 #对feed进行计数
	for sec_or_media, url, title, content,brief in redbook.Items():
		if sec_or_media.startswith(r'image/'):
			filename = path.join(ROOT, 'temp',title)
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
			}

			data[i]['entries'].append(local_entry)

	wrap ={
		'date': date.today().isoformat(),
		'feeds':data,
		'img_nums':redbook._imgindex,
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
		render_and_write('feed.html',feed,'%s.html' % feed['number'],output_dir,templates_env)


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

