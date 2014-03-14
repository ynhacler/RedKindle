# -*- coding:utf-8 -*-

import web
import datetime
import memcache,hashlib

#链接数据库
db = web.database(dbn='mysql',db='redkindle',user='root',pw='1q2w3e',charset='utf8')

#缓存
memc = memcache.Client(['127.0.0.1:11211'],debug=0)

#建立一个简单hash算法函数
def hash(obj):
	m=hashlib.md5()
	m.update(obj)
	key=m.hexdigest()
	return key

#是否有此用户
def isuser(name,pw):
	try:
		myvar = dict(name=name,pw=pw)
		result = db.select('kinuser',myvar,where ='name = $name and passwd = $pw')
		if len(result) > 0:
			return 1
		else:
			return 0
	except IndexError:
		return 0

#用户查询
def getuser(name):
	try:
		result = memc.get(hash('kinuser%s' % name))
		if not result:
			myvar = dict(name=name)
			result = list(db.select('kinuser',myvar,where='name = $name'))
			memc.add(hash('kinuser%s' % name),result,time=60*4)
		return result
	except:
		return None

#是否存在次用户
def ifhasuser(name,kindle_email):
	try:
		myvar = dict(name=name,ke=kindle_email+'%')
		#result = db.select('kinuser',myvar,where ="name = $name and kindle_email like \%$ke\%",_test=False)
		result = db.query("SELECT * FROM kinuser WHERE name = $name and kindle_email like $ke",vars=myvar)
		if len(result) > 0:
			return 1
		else:
			return 0
	except IndexError:
		return 0

#得到对应用户的feeds
def userid2feeds(user_id):
	try:
		myvar = dict(k_id=user_id)
		result = db.select('feeds_user',myvar,where='k_id = $k_id',limit=10)
		feeds = []
		for n in result:
			feeds.append(n.f_id)

		return feeds
	except:
		return []

#得到用户的feeds根据name
def username2feeds(username):
	try:
		'''
		myvar=dict(name=username)
		result = db.select('kinuser',myvar,where='name=$name')
		'''
		result = getuser(username)
		k_id = result[0].k_id
		return userid2feeds(k_id)
	except:
		return []


#得到所有feeds信息
def get_allbooks():
	try:
		value = memc.get(hash('feeds'))
		if not value:
			value = list(db.select('feeds'))
			memc.add(hash('feeds'),value,time=60*5)
		return value
	except:
		return []

#等到类别信息
def get_category():
	try:
		result = memc.get(hash('cate'))
		if not result:
			result = list(db.select('category'))
			memc.add(hash('cate'),result,time=60*60*5)
		return result
	except:
		return []

#得到用户列表
def get_all_users(offset,limit):
	try:
		result = db.select('kinuser',offset=offset,limit=limit)
		return result
	except:
		return []

#得到用户数
def get_user_num():
	try:
		result = memc.get(hash('count'))
		if not result:
			result = db.query('select count(*) as count from kinuser')[0]
			memc.add(hash('count'),result,time=60*60)
		return result
	except:
		return 0


#添加feed
def put_feed(title,url,isfull,descrip,cate,update_cycle=6):
	try:
		re_id = db.insert('feeds', title=title,url=url,isfulltext=isfull,descrip=descrip,c_id=cate,update_cycle=update_cycle)
		return re_id
	except:
		return -1

#删除feed
def delete_feed(id):
	try:
	#feeds
		myvar = dict(f_id=id)

                db.delete('feeds', where=web.db.sqlwhere(myvar))
	#feed_user
		db.delete('feeds_user', where=web.db.sqlwhere(myvar))
		memc.delete(hash('feeds'),time=2)
                return 1
	except:
		return 0

#删除旧文章
def delete_old_article(id):
	try:
		myvar = dict(f_id=id)
		db.delete('rss_gain', where=web.db.sqlwhere(myvar))
		return 1
	except:
		return 0

#是否存在这本书
def ifhasbook(id):
	try:
		myvar = dict(f_id=id)
		result = db.select('feeds',myvar,where='f_id=$f_id')
		if len(result)>0:
			return 1
		else:
			return 0
	except:
		return 0

#添加订阅
def put_subscribe(k_id,id):
	#判断是否已经订阅
	try:
		myvar = dict(k_id=k_id,f_id=id)
		result = db.select('feeds_user',myvar,where='k_id=$k_id and f_id=$f_id')
		if len(result) > 0:
			return 0
		db.insert('feeds_user',k_id=k_id,f_id=id)
		return 1
	except:
		return 0

#取消订阅
def put_unsubscribe(k_id,id):
	try:
		myvar = dict(k_id=k_id,f_id=id)

		db.delete('feeds_user', where=web.db.sqlwhere(myvar))
		return 1
	except:
		return 0

#用户信息更新
def put_user_messgaes(k_id,name,kindle_email,send_time=1,enable_send=0,keep_image=0,timezone=8,days=[0],ifmobi=1):
	#db.update('user', where='id=$id', vars={'id':100}, name='Michael', age=29)
	try:
		myvar = dict(k_id=k_id)
		bin_re = 0
                if u'0' not in days:
			for d in days:
				bin_temp = int(bin(1)[2:]) << int(d)
				bin_re |= bin_temp
		else:
			bin_re = int(bin(0)[2:])

		db.update('kinuser',where='k_id=$k_id',vars=myvar,kindle_email=kindle_email,send_time=send_time,enable_send=enable_send,keep_image=keep_image,timezone=timezone,send_days=bin_re,ifmobi=ifmobi,_test=False)
		memc.delete(hash('kinuser%s' % name))
		return 1
	except:
		return 0

#改密码
def update_user_passwd(k_id,passwd):
	try:
		myvar = dict(k_id=k_id)
		db.update('kinuser',where='k_id=$k_id',vars=myvar,passwd = passwd)
		return 1
	except:
		return 0

#重置密码
def resetpw(name,p1):
	try:
		myvar = dict(name=name)
		db.update('kinuser',where='name=$name',vars=myvar,passwd = p1)
		return 1
	except:
		return 0

#登录时间	
def update_logintime(local_time,name):
	try:
		myvar = dict(name=name)
		db.update('kinuser',where='name=$name',vars=myvar,login_time = local_time)
		return 1
	except:
		return 0

#查询当前时间的可推送用户
def get_current_push_users(hour,weekday):
	try:
		weekday = int(bin(1)[2:]) << weekday
		myvar = dict(hour=hour,weekday = weekday)
		result = db.select('kinuser',myvar,where='send_time=(timezone+$hour)%24 and enable_send = 1 and (send_days = 0 or ($weekday & send_days != 0))',_test=False)
		return result
	except:
		return []

#插入新用户
def input_user(user,passwd):
	db.insert('kinuser',name =user,passwd=passwd)

#修改发送日期
def update_send_days(k_id,days):
	try:
		myvar = dict(k_id=k_id)
		bin_re = 0
		if 0 not in days:
			for d in days:
				bin_temp = int(bin(1)[2:]) << d
				bin_re |= bin_temp

		db.update('kinuser',where='k_id=$k_id',vars=myvar,send_days = bin_re)
		return 1
	except:
		return 0

#取得发送日期
def get_send_days(id):
	myvar = dict(k_id=id)
	result = db.select('kinuser',myvar,where='k_id=$k_id')
	return result

#把文章放入mysql
def put_section_article(f_id,sec_or_media, url,title, content,brief):
	try:
		db.insert('rss_gain',f_id=f_id,
			time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			section=sec_or_media,
			url=url,
			title=title,
			content=content,
			brief=brief)
	except:
		return 0

#改变文章更新时间
def update_article_update_time(f_id):
	try:
		myvar = dict(f_id=f_id)
		db.update('feeds',where='f_id=$f_id',vars=myvar,last_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		return 1
	except:
		return 0

#得到文章
def get_article2id(feed_id):
	try:
		result = memc.get(hash('rss_gain%s' % feed_id))
		if not result:
			myvar = dict(f_id=feed_id)
			result = list(db.select('rss_gain',myvar,where='f_id=$f_id'))
			qq=memc.add(hash('rss_gain%s' % feed_id),result,time=60*5)
		return result
	except:
		return []


if __name__ == "__main__":
	print getuser(name='zzh')[0].passwd
#	print userid2feeds(2)
#	print list(get_allbooks())
#	put_feed('aa','aaa')
#	print ifhasbook(100)
#	print put_subscribe(1,2)
#	print put_unsubscribe(1,2)
#	print put_user_messgaes(1,'zzh@126.com',23,int(True),int(False),-12)
#	print int(True)
#	print username2feeds('zzh')
#	print len(get_current_push_users(9,1))
#	input_user('zz@11.com','1q2w3e')
#	update_send_days(2,[4,7])
#	print get_all_users()[0]
#	print get_send_days(2)[0].send_days
#	print ifhasuser('qq','zzh')
#	print resetpw('zz12@11.com','1q2w3e')
#memc.set('foo','bar')
#	print memc.get('foo')
#	print get_category()
#	print get_user_num()
#	get_article2id(17)
