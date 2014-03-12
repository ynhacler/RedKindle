RedKindle
================================

Kindle期刊推送系统
http://zhred.net

系统为Linux （Debian或Ubuntu）


一、Python版本2.7.3，不支持3.0+。


二、安装数据库：<br/>
apt-get install mysql-server<br/>

进入MySql：<br/>
mysql -u root -p<br/>
show databases;<br/>
create database redkindle;<br/>

退出后，导入数据：<br/>
mysql -u root -p redkindle < abc.sql<br/>

连接数据库：<br/>
进入model.py，在第7行设置帐号密码。<br/>


安装依赖库：<br/>
apt-get install python-pip<br/>
apt-get install python-dev<br/>
apt-get install build-essential<br/>
apt-get install libmysqld-dev<br/>
apt-get install libmysqlclient-dev<br/>
pip install mysql-python（成功后出现：Successfully installed mysql-python）<br/>


测试数据库连接：<br/>
进入项目目录：python model.py<br/>
看是否会报错。无错误就是配置成功。<br/>


三、安装其他依赖库：<br/>
pip install jinja2<br/>
apt-get install python-lxml<br/>
apt-get install redis-server<br/>
apt-get install python-redis<br/>
pip install python-memcached<br/>
apt-get install memcached<br/>
pip install requests<br/>
pip install redis<br/>
pip install rq(简单的python任务队列，http://python-rq.org/)<br/>
apt-get install libjpeg8-dev<br/>
apt-get install libpng12-dev<br/>
apt-get install libfreetype6-dev<br/>
apt-get install zlib1g-dev<br/>

定位*.so文件位置：<br/>
find / -name libz.so（我的32位debian在：/usr/lib/i386-linux-gnu/）<br/>
编辑/etc/ld.so.conf，把 /usr/lib/i386-linux-gnu/（各主机不一样） 加到文件末尾，再执行一次ldconfig,让配置生效<br/>

pip uninstall pil<br/>
pip install pillow<br/>
<br/>
安装后，下面不能出现not。<br/>
*** JPEG support not available<br/>
*** ZLIB (PNG/ZIP) support not available<br/>
*** FREETYPE2 support not available<br/>



四、在项目目录里建立temp文件夹。<br/>

运行python bmaintest.py，出现http://0.0.0.0:8080/。进入浏览器访问看是否正常。<br/>

管理员用户设置：<br/>
创建普通用户，进入数据库。把用户的level设置为3就行。<br/>



五、定时投送设置：<br/>
不用安装软件，用系统自带的cron定时器：<br/>
http://blog.sina.com.cn/s/blog_62d12d690101dase.html 有简单配置。<br/>
详细使用请google。<br/>

六、邮件系统：<br/>
安装postfix(系统自带exim4，不好用直接删了)，就可以使用。详细使用google。<br/>
不想安装，进入pushworker.py，在send_mail函数里进行设置。<br/>


七、使用：<br/>
1. command & ： 后台运行，你关掉终端会停止运行<br/>
2. nohup command & ： 后台运行，你关掉终端也会继续运行<br/>

rq是个任务队列管理器，必须一直运行。所以系统正常运行会有两个进程。<br/>

nohup python bmaintest &<br/>
nohup python worker.py &<br/>


--------------------------------------------------------------------<br/>
如果出现编码错误，可以运行：<br/>
	export LANG="en_US.UTF-8"<br/>
	export LC_ALL="en_US.UTF-8"<br/>

我的服务器：<br/>
	nginx + uwsgi + web.py<br/>

rq监控命令：<br/>
	rqinfo<br/>
	rq-dashboard<br/>


=======程序结构=================================<br/>
web => web.py库<br/>
dateutil => py时间插件库<br/>
bs4 => BeautifulSoup库<br/>
lib/feedparser.py => feedparser库<br/>
lib/readability => 非正文内容剔除掉，留下最有用的信息。依附BeautifulSoup    库<br/>
cssutils => cssutils库 解析和构建css<br/>
CSSSelector => CSSSelector库 css转xml<br/>
chardet => 实现字符串/文件的编码检测<br/>
urlopener.py => 处理错误URL和cookie情况<br/>
bmaintest.py => 主函数<br/>
abc.sql => 数据库<br/>
config.py => 配置文件<br/>
templates_web => 网页<br/>
cronpush.py => 定时推送模块<br/>
templates2 => 电子书生成模型xml<br/>
pushworker.py => 电子书生成，投递模块<br/>
books => 书籍模块<br/>
kindlegen_1.1 => 生产mobi的程序<br/>
worker.py => rq任务器<br/>
rq2 => rq库<br/>
static => 网站静态文件<br/>
temp => 临时文件夹<br/>
model.py => 数据库操作模块<br/>
<br/>
其它文件夹基本没用。<br/>


--------------------------------<br/>
RSS存在feeds表中，普通源地址直接填在url里，单独写的针对某一网站的抓取，填模块名。<br/>


