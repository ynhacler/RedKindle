#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Version__ = "1.0"
__Author__ = "ynhacler"


import os, datetime, logging, __builtin__, hashlib, time
from collections import OrderedDict, defaultdict
import gettext
import memcache

from os import path


# for debug
log = logging.getLogger()
__builtin__.__dict__['default_log'] = log

import web
import jinja2
from bs4 import BeautifulSoup
import model

from config import *

#设置编码方式
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#调试模式
#session不能工作在debug模式
web.config.debug = False


#from books import BookClasses, BookClass
from books.base import BaseFeedBook,  BaseUrlBook

#使用rq任务队列
from rq2 import Queue,use_connection
from worker import conn
from pushworker import pushwork,send_mail,pushwork3

#%Y-%m-%d %H:%M:%S
def local_time(fmt="%Y-%m-%d %H:%M:%S", tz=TIMEZONE):
	return (datetime.datetime.utcnow()+datetime.timedelta(hours=tz)).strftime(fmt)

def hide_email(email):
	""" 隐藏真实email地址，使用星号代替部分字符，适用于4位字符以上 """
	email = email.split('@')
	to = email[0][0:2] + ''.join(['*' for s in email[0][2:-1]]) + email[0][-1]
	return to + '@' + email[-1]

def set_lang(lang):
	""" 设置网页显示语言 """
	tr = gettext.translation('lang', 'i18n', languages=[lang])
	tr.install(True)
	jjenv.install_gettext_translations(tr)

#基础类
class BaseHandler:
	@classmethod
	def logined(self):
		return True if session.login == 1 else False

	#检查session是否登录
	def login_required(self, username=None):
		if (session.login == 0) or (username and username != session.username):
			raise web.seeother(r'/')

	#检查是否有此用户
	def getcurrentuser(self):
		self.login_required()
		u = model.getuser(session.username)
		if not u:
			raise web.seeother(r'/')
		return u[0]




#主页
class Home(BaseHandler):
	def GET(self):
		return jjenv.get_template('home.html').render(nickname=session.username,title="Home")

class Help():
	def GET(self):
		return jjenv.get_template('help.html').render()

#登录
class Login(BaseHandler):
	def GET(self):
		tips = "请输入邮箱地址和密码。"

		if session.login == 1:#是否登录
			web.seeother(r'/')
		else:
			return jjenv.get_template("login.html").render(nickname='',title='Login',tips=tips)

	def POST(self):
		name, passwd = web.input().get('u'), web.input().get('p')
		if name.strip() == '':
			tips = "地址为空！"
			return jjenv.get_template("login.html").render(nickname='',title='Login',tips=tips)
		elif len(name) > 35:
			tips = "地址过长!"
			return jjenv.get_template("login.html").render(nickname='',title='Login',tips=tips,username=name)
		elif '<' in name or '>' in name or '&' in name:
			tips = "包含非法字符!"
			return jjenv.get_template("login.html").render(nickname='',title='Login',tips=tips)
		pwdhash = hashlib.md5(passwd).hexdigest()

		if model.isuser(name,pwdhash) == 1:
			session.login = 1
			session.username = name
			#Login_time
			model.update_logintime(local_time(),name)
			raise web.seeother(r'/')
		else:
			tips = "帐号不存在或密码错误!"
			session.login = 0
			session.username = ''
			return jjenv.get_template("login.html").render(nickname='',title='Login',tips=tips,username=name)

#忘记密码后重置
class ResetPW(BaseHandler):
	def POST(self):
		name = web.input().get('u').strip()
		p1 = web.input().get('p1').strip()
		p2 = web.input().get('p2').strip()

		if p1 != p2:
			tips = "两次输入不一致！"
			return jjenv.get_template("reset_passwd.html").render(nickname=name,title='reset_passwd',tips=tips)

		if len(p1)<4:
			tips = "密码太短！"
			return jjenv.get_template("reset_passwd.html").render(nickname=name,title='reset_passwd',tips=tips)

		p1 = hashlib.md5(p1).hexdigest()
		re = model.resetpw(name,p1)

		if re == 1:
			tips = "重置成功！"
			return jjenv.get_template("forget_passwd.html").render(nickname='',title='forget_passwd',tips=tips)
		else:
			tips = "出错！"
			return jjenv.get_template("reset_passwd.html").render(nickname=name,title='reset_passwd',tips=tips)

#忘记密码
class ForgetPW(BaseHandler):
	def GET(self):
		tips = "请输入邮箱地址和kindle地址。"
		if session.login == 1:#是否登录
			web.seeother(r'/')
		else:
			return jjenv.get_template("forget_passwd.html").render(nickname='',title='forget_passwd',tips=tips)

	def POST(self):
		name = web.input().get('u')
		kindle_email = web.input().get('k')
		#检查合法性
		if name.strip() == '' or kindle_email.strip() == '' or len(kindle_email.strip())<3:
			tips = "输入有误！"
			return jjenv.get_template("forget_passwd.html").render(nickname='',title='forget_passwd',tips=tips)

		if model.ifhasuser(name,kindle_email) == 1:
			return jjenv.get_template("reset_passwd.html").render(nickname=name,title='reset_passwd')
		else:
			tips = "帐号不存在或输入错误!"
			return jjenv.get_template("forget_passwd.html").render(nickname='',title='forget_passwd',tips=tips)


#退出登录
class Logout(BaseHandler):
	def GET(self):
		session.login = 0
		session.username = ''
		session.kill()
		raise web.seeother(r'/')

#管理我的订阅和杂志列表
class MySubscription(BaseHandler):
	def GET(self,tips=None):
		user = self.getcurrentuser()
		#所有RSS源和已订阅的源
		ownfeeds = model.userid2feeds(user.k_id) if user else None
		books = list(model.get_allbooks())#webpy返回的是storage对象，用一次就不见了
		category = list(model.get_category())
		return jjenv.get_template("my.html").render(nickname=session.username,current='my',title='My subscription',books=books,ownfeeds=ownfeeds,tips=tips,level=user.level,cate=category)

	def POST(self):#添加自定义RSS
		user = self.getcurrentuser()
		title = web.input().get('t')
		url = web.input().get('url')
		isfulltext = int(bool(web.input().get('full')))
		description = web.input().get('descrip')
		category = int(web.input().get('category'))
		update_cycle = web.input().get('up_t')
		if update_cycle == '':
			update_cycle = 6
		else:
			update_cycle = int(update_cycle)

		if not title or not url:
			return self.GET('title or url is empty!')
		#添加
		id = model.put_feed(title,url,isfulltext,description,category,update_cycle)

		if id != -1:
			#创建文件夹
			ROOT = path.dirname(path.abspath(__file__))
			output_dir = path.join(ROOT, 'temp')#%s' % id
			output_dir = path.join(output_dir,'feed_%s' % id)
			isExists = path.exists(output_dir)
			if not isExists:
				os.makedirs(output_dir)

		raise web.seeother('/my')

#已经订阅的
class MyExistSub(BaseHandler):
	def GET(self,tips=None):
		user = self.getcurrentuser()
		ownfeeds = model.userid2feeds(user.k_id) if user else None
		books = list(model.get_allbooks())#webpy返回的是storage对象，用一次就不见了
		category = list(model.get_category())
		return jjenv.get_template("mysub.html").render(nickname=session.username,current='mysub',title='My subscription',books=books,ownfeeds=ownfeeds,tips=tips,level=user.level,cate=category)

#订阅
class Subscribe(BaseHandler):
	def POST(self, id):
		self.login_required()
		if not id:
			return "the id is empty!<br />"
		try:
			id = int(id)
		except:
			return "the id is invalid!<br />"
		#判断书id是否正确
		b = model.ifhasbook(id)
		if b == 0:
			return "the book(%d) not exist!<br />" % id


		#订阅(判断是否已经订阅)
		user = self.getcurrentuser()
		model.put_subscribe(user.k_id,id)

		#raise web.seeother('/my')
		return 'ok'

#取消订阅
class Unsubscribe(BaseHandler):
	def POST(self, id):
		self.login_required()
		if not id:
			return "the id is empty!<br />"
		try:
			id = int(id)
		except:
			return "the id is invalid!<br />"

		#判断书id是否正确
		b = model.ifhasbook(id)
		if b == 0:
			return "the book(%d) not exist!<br />" % id


		#取消订阅(判断是否已经订阅)
		user = self.getcurrentuser()
		model.put_unsubscribe(user.k_id,id)

		#raise web.seeother('/mysub')
		return 'ok'

#管理员删除feed
class Deletefeed(BaseHandler):
	def GET(self,id):
		self.login_required()
		if not id:
			return "the id is empty!<br/>"
		try:
			id = int(id)
		except:
			return "the id is invalid!<br/>"

		#判断书id是否正确
		b = model.ifhasbook(id)
                if b == 0:
			return "the book(%d) not exist!<br />" % id

		model.delete_feed(id)

		raise web.seeother('/my')

#管理页面
class Admin(BaseHandler):
	def GET(self,page=1):
		user = self.getcurrentuser()
		#fen ye
		if user.level == 3:
			page = int(page)
			perpage = 20
			offset = (page - 1) * perpage
			users = model.get_all_users(offset=offset,limit=perpage)
			users_count = model.get_user_num()

			pages = users_count.count / perpage

			if users_count.count % perpage > 0:
				pages += 1
			if page > pages:
				raise web.seeother('/admin')
		else:
			users = None
			pages = 0

		return jjenv.get_template('admin.html').render(nickname=session.username,title="Admin", current='admin', user=user, users=users, pages = pages)

	def POST(self):
		op,p1,p2 = web.input().get('op'), web.input().get('p1'), web.input().get('p2')
		user = self.getcurrentuser()
		if user.level == 3:
			page = 1
			perpage = 20
			offset = (page - 1) * perpage
			users = model.get_all_users(offset=offset,limit=perpage)
			users_count = model.get_user_num()
			pages = users_count.count / perpage
			if users_count.count % perpage > 0:
				pages += 1
		else:
			users = None
			pages = 0

		if op is not None and p1 is not None and p2 is not None: #修改密码
			if user.passwd != hashlib.md5(op).hexdigest():
				tips = "原密码错误！"
			elif p1 != p2:
				tips = "两次密码不一致！"
			else:
				tips = "修改成功！"
				passwd = hashlib.md5(p1).hexdigest()
				model.update_user_passwd(user.k_id,passwd)
			return jjenv.get_template('admin.html').render(nickname=session.username,title="Admin",current='admin',user=user,users=users,chpwdtips=tips,pages = pages)
		else:
			return self.GET()

#设置页面
class Setting(BaseHandler):
	def GET(self,method=False):
		user = self.getcurrentuser()

		#days_convent
		days = user.send_days
		days_convent = []
		if days == 0:
			days_convent.append(0)
		else:
			for i in range(1,8):
				if days & int(bin(1 << i),2) != 0:
					days_convent.append(i)
		user.send_days = days_convent

		return jjenv.get_template('setting.html').render(nickname=session.username,title="Setting",current='setting',user=user,mail_sender=SrcEmail,method=method)

	def POST(self):
		user = self.getcurrentuser()
		kindle_email = web.input().get('kindle_email').strip()
		timezone = int(web.input().get('timezone'))
		send_time = (web.input().get('send_time'))
		ifmobi = int(web.input().get('book_type'))
		enable_send = int(bool(web.input().get('enable_send')))
		keep_image = int(bool(web.input().get("keepimage")))
		send_days = web.input(optionday=[]).get('optionday')
		if len(send_days) == 0:
			send_days = [u'0']

		test_code = ['<','>','*','#','%','&']
		for t_c in test_code:
			if t_c in kindle_email:
				kindle_email = ''
		if '@' not in kindle_email or '.' not in kindle_email or kindle_email.strip() == '':
			kindle_email = ''
			enable_send = 0


		#用户信息设置
		#put_user_messgaes(k_id,kindle_email,send_time=1,enable_send=0,keep_image=0,timezone=8,days=[0])
		result = model.put_user_messgaes(user.k_id,user.name,kindle_email,send_time,enable_send,keep_image,timezone,send_days,ifmobi)

		'''
		print kindle_email
		print send_time
		print enable_send
		print keep_image
		print timezone
		print send_days
		'''

		raise web.seeother('')#刷新
		#return jjenv.get_template('setting.html').render(nickname=session.username,title="Setting",current='setting',user=user,mail_sender=SrcEmail,success=success)

#注册
class Register(BaseHandler):
	def GET(self):
		if session.login == 1:#是否登录
			web.seeother(r'/')
		else:
			return jjenv.get_template("register.html").render(nickname='',title='Register')


	def POST(self):
		name = web.input().get('u')
		passwd = web.input().get('p')

		#检查是否已存在，格式问题
		if name.strip() == '' or passwd.strip() == '':
			tips = "不能为空!"
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips=tips)
		elif '@' not in name or '.' not in name == '':
			tips = "地址有误！"
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips=tips)
		elif len(name) > 50:
			tips = "地址太长!"
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips=tips,username=name)
		elif '<' in name or '>' in name or '&' in name:
			tips = "含有非法字符!"
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips=tips)
		elif len(passwd.strip())<4:
			tips = "密码太短！"
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips=tips)

		u = model.getuser(name)
		if u:
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips="用户已存在!")
		#注册
		model.input_user(name,hashlib.md5(passwd).hexdigest())

		#返回登录界面
		#raise web.seeother(r'/')

		#注册成功直接登录
		pwdhash = hashlib.md5(passwd).hexdigest()
		if model.isuser(name,pwdhash) == 1:
			session.login = 1
			session.username = name
			raise web.seeother(r'/')
		else:
			return jjenv.get_template("register.html").render(nickname='',title='Register',tips="")

class FeedBack(BaseHandler):
	def GET(self):
		return jjenv.get_template("feedback.html").render(nickname=session.username,title='Feedback',current='feedback')

class Test(BaseHandler):
	def GET(self):
		s = ''
		for d in os.environ:
			s += "<pre><p>" + str(d).rjust(28) + " | " + str(os.environ[d]) + "</p></pre>"
		return s


#推送
class Deliver(BaseHandler):
	def GET(self):
		username = web.input().get('u')
		adminpush = web.input().get('p')

		if username and adminpush != None:#用于管理员测试
			#搜索自动处理的feed(字符串http开头)
			feeds = []
			#搜索手动处理的feed
			mfeeds = []
			feeds_num = 0
			ownfeeds = model.username2feeds(username)
			if len(ownfeeds) != 0:
				'''
				#取feeds信息
				books = (model.get_allbooks())
				for book in books:
					if book.f_id in ownfeeds:
						b=[]
						if cmp('http',book.url[0:4].lower()) == 0:
							b.append(book.title)
							b.append(book.url)
							if book.isfulltext == 1:
								b.append(True)
							else:
								b.append(False)
							feeds.append(b)
						else:
							b.append(book.url)
							mfeeds.append(b)
						feeds_num += 1
				#取用户信息
				user = model.getuser(username)[0]
				#加入eq
				if user and user.kindle_email:
					jobq.enqueue(pushwork,args=(user.kindle_email,feeds,mfeeds,user.keep_image),timeout=feeds_num*300)
				'''
				user = model.getuser(username)[0]
				if user and user.kindle_email:
					jobq.enqueue(pushwork3,args=(user.kindle_email,ownfeeds,user.keep_image,user.ifmobi))
			return jjenv.get_template("autoback.html").render(nickname=session.username,title='Delivering',tips='admin已投递！')
		else:
			user = model.getuser(username)[0]
			if user and user.kindle_email:
				ROOT = path.dirname(path.abspath(__file__))
				output_dir = path.join(ROOT, 'templates2')
				mobi_file = path.join(output_dir,'WelcomeRedKindle.mobi')
				jobq.enqueue(send_mail,SrcEmail,user.kindle_email,mobi_file)
			return jjenv.get_template("autoback.html").render(nickname=session.username,title='Delivering',tips='已投递！')

#=====================================================
urls = (
	r"/", "Home",
	"/help","Help",
	"/login","Login",
	"/logout", "Logout",
	"/my", "MySubscription",
	"/subscribe/(.*)", "Subscribe",
	"/unsubscribe/(.*)", "Unsubscribe",
	"/setting", "Setting",
	"/deliver", "Deliver",
	"/register","Register",
	"/admin","Admin",
	"/admin/page/(\d+)","Admin",
	"/delfeed/(.*)","Deletefeed",
	"/feedback", "FeedBack",
	"/test", "Test",
	"/mysub","MyExistSub",
	"/forget_passwd","ForgetPW",
	"/reset_password","ResetPW",
)

app = web.application(urls,globals())

#缓存设置
class MemCacheStore(web.session.Store):#特别注意是这，重载了下web.py的 Store类，来实现memcached的操作
	mc = None
	def __init__(self):
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
	def __contains__(self, key):
		return self.mc.get(key) != None
	def __getitem__(self, key):
		return self.mc.get(key)
	def __setitem__(self, key, value):
		self.mc.set(key, value, time = web.config.session_parameters["timeout"])
	def __delitem__(self, key):
		self.mc.delete(key)
	def cleanup(self, timeout):
		pass # Not needed as we assigned the timeout to memcache

#memcache
session = web.session.Session(app, MemCacheStore(),initializer={'username':'','login':0})
#普通
#session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'username':'','login':0})

jjenv = jinja2.Environment(loader=jinja2.FileSystemLoader('templates_web'),extensions=["jinja2.ext.do",])

use_connection(conn)

jobq = Queue()


if __name__ == "__main__":
	app.run()
else:
	application=app.wsgifunc()
