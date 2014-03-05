RedKindle
================================

Kindle期刊推送系统
http://zhred.net

系统为Linux （Debian或Ubuntu）


一、Python版本2.7.3，不支持3.0+。


二、安装数据库：
apt-get install mysql-server

进入MySql：
mysql -u root -p
show databases;
create database redkindle;

退出后，导入数据：
mysql -u root -p redkindle < abc.sql

连接数据库：
进入model.py，在第7行设置帐号密码。


安装依赖库：
apt-get install python-pip
apt-get install python-dev
apt-get install build-essential
apt-get install libmysqld-dev
apt-get install libmysqlclient-dev
pip install mysql-python（成功后出现：Successfully installed mysql-python）


测试数据库连接：
进入项目目录：python model.py
看是否会报错。无错误就是配置成功。


三、安装其他依赖库：
pip install jinja2
apt-get install python-lxml
apt-get install redis-server
apt-get install python-redis
pip install requests
pip install redis
pip install rq()
apt-get install libjpeg8-dev
apt-get install libpng12-dev
apt-get install libfreetype6-dev
apt-get install zlib1g-dev

定位*.so文件位置：
find / -name libz.so（我的32位debian在：/usr/lib/i386-linux-gnu/）
编辑/etc/ld.so.conf，把 /usr/lib/i386-linux-gnu/（各主机不一样） 加到文件末尾，再执行一次ldconfig,让配置生效

pip uninstall pil
pip install pillow

安装后，下面不能出现not。
*** JPEG support not available
*** ZLIB (PNG/ZIP) support not available
*** FREETYPE2 support not available



四、在项目目录里建立temp文件夹。

运行python bmaintest.py，出现http://0.0.0.0:8080/。进入浏览器访问看是否正常。

管理员用户设置：
创建普通用户，进入数据库。把用户的level设置为3就行。



五、定时投送设置：
不用安装软件，用系统自带的cron定时器：
http://blog.sina.com.cn/s/blog_62d12d690101dase.html 有简单配置。
详细使用请google。

六、邮件系统：
安装postfix(系统自带exim4，不好用直接删了)，就可以使用。详细使用google。
不想安装，进入pushworker.py，在send_mail函数里进行设置。


七、使用：
1. command & ： 后台运行，你关掉终端会停止运行
2. nohup command & ： 后台运行，你关掉终端也会继续运行

rq是个任务队列管理器，必须一直运行。所以系统正常运行会有两个进程。

nohup python bmaintest &
nohup python worker.py &


--------------------------------------------------------------------
如果出现编码错误，可以运行：
	export LANG="en_US.UTF-8"
	export LC_ALL="en_US.UTF-8"

我的服务器：
	nginx + uwsgi + web.py

rq监控命令：
	rqinfo
	rq-dashboard


=======程序结构=================================
web => web.py库
dateutil => py时间插件库
bs4 => BeautifulSoup库
lib/feedparser.py => feedparser库
lib/readability => 非正文内容剔除掉，留下最有用的信息。依附BeautifulSoup    库
cssutils => cssutils库 解析和构建css
CSSSelector => CSSSelector库 css转xml
chardet => 实现字符串/文件的编码检测
urlopener.py => 处理错误URL和cookie情况
bmaintest.py => 主函数
abc.sql => 数据库
config.py => 配置文件
templates_web => 网页
cronpush.py => 定时推送模块
templates2 => 电子书生成模型xml
pushworker.py => 电子书生成，投递模块
books => 书籍模块
kindlegen_1.1 => 生产mobi的程序
worker.py => rq任务器
rq2 => rq库
static => 网站静态文件
temp => 临时文件夹
model.py => 数据库操作模块

其它文件夹基本没用。


--------------------------------
RSS存在feeds表中，普通源地址直接填在url里，单独写的针对某一网站的抓取，填模块名。


