# -*- coding:utf-8 -*-

import web
import datetime

#链接数据库
db = web.database(dbn='mysql',db='redkindle',user='root',pw='1q2w3e')

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
		myvar = dict(name=name)
		result = db.select('kinuser',myvar,where='name = $name')
		return result
	except:
		return None

#得到对应用户的feeds
def userid2feeds(user_id):
	try:
		myvar = dict(k_id=user_id)
		result = db.select('feeds_user',myvar,where='k_id = $k_id')
		feeds = []
		for n in result:
			feeds.append(n.f_id)

		return feeds
	except:
		return []

#得到用户的feeds根据name
def username2feeds(username):
	try:
		myvar=dict(name=username)
		result = db.select('kinuser',myvar,where='name=$name')
		k_id = result[0].k_id
		return userid2feeds(k_id)
	except:
		return []


#得到所有feeds信息
def get_allbooks():
	try:
		result = db.select('feeds')
		return result
	except:
		return []

#等到类别信息
def get_category():
	try:
		result = db.select('category')
		return result
	except:
		return []

#得到用户列表
def get_all_users():
	try:
		result = db.select('kinuser')
		return result
	except:
		return []


#添加feed
def put_feed(title,url,isfull,descrip,cate):
	db.insert('feeds', title=title,url=url,isfulltext=isfull,descrip=descrip,c_id=cate)

#删除feed
def delete_feed(id):
	try:
	#feeds
		myvar = dict(f_id=id)

                db.delete('feeds', where=web.db.sqlwhere(myvar))
	#feed_user
		db.delete('feeds_user', where=web.db.sqlwhere(myvar))
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
def put_user_messgaes(k_id,kindle_email,send_time=1,enable_send=0,keep_image=0,timezone=8):
	#db.update('user', where='id=$id', vars={'id':100}, name='Michael', age=29)
	try:
		myvar = dict(k_id=k_id)
		db.update('kinuser',where='k_id=$k_id',vars=myvar,kindle_email=kindle_email,send_time=send_time,enable_send=enable_send,keep_image=keep_image,timezone=timezone,_test=False)
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
#登录时间	
def update_logintime(local_time,name):
	try:
		myvar = dict(name=name)
		db.update('kinuser',where='name=$name',vars=myvar,login_time = local_time)
		return 1
	except:
		return 0

#查询当前时间的可推送用户
def get_current_push_users(hour):
	try:
		myvar = dict(hour=hour)
		result = db.select('kinuser',myvar,where='send_time=(timezone+$hour)%24 and enable_send = 1',_test=False)
		return result
	except:
		return 0

#插入新用户
def input_user(user,passwd):
	db.insert('kinuser',name =user,passwd=passwd)

if __name__ == "__main__":
#	print getuser(name='zzh')[0].passwd
#	print userid2feeds(2)
#	print get_allbooks()[1]
#	put_feed('aa','aaa')
#	print ifhasbook(100)
#	print put_subscribe(1,2)
#	print put_unsubscribe(1,2)
#	print put_user_messgaes(1,'zzh@126.com',23,int(True),int(False),-12)
#	print int(True)
#	print username2feeds('zzh')
#	print get_current_push_users(19)[0]
	input_user('zz@11.com','1q2w3e')
