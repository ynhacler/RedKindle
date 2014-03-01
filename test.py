from lib.img import rescale_image
from lib.url_req import URLOpener
import os

#rescale_image(data, maxsizeb=4000000, dimen=None, png2jpg=False,     graying=True, reduceto=(600,800)):


test = URLOpener().open('http://img.xinjunshi.com/uploads/allimg/140224/11-140224101225.jpg')
#test=URLOpener().open('http://www.sucaitianxia.com/d/file/20131222/28caa29d1ddad3c085035e024a9f0b02.png')
con = test.content

con = rescale_image(con,reduceto=(400,600),graying=False)
fout = open('zzh.jpg', "wb")
fout.write(con)
fout.close()

