from PIL import Image
from hashlib import sha1
from datetime import datetime
from struct import unpack
import os ,tempfile
OX =lambda num :1 if num else 0
def gethashtuple (im ):
	sh =sha1 ()
	sh .update (im .tobytes ())
	sh .update (bytes (str (datetime .now ()),'utf8'))
	return unpack ("IIIII",sh .digest ())
def getox (hashtuple ,ii ,level ):
	if level in (1 ,2 ):
		if ii %{1 :2 ,2 :3 ,3 :7 }[level ]==0 :return 0
	else :
		pass
	n =ii %5
	m =ii %32
	return hashtuple [n ]&(1 <<m )
def pxset (px ,px2 ,x ,y ,hashtuple ,mx2 ,level ):
	ii =(mx2 *(y -1 ))+(x -1 )
	ox =getox (hashtuple ,ii ,level )
	if ox ==0 :
		return
	tpx =OX (px [x ,y -1 ])
	bpx =OX (px [x ,y +1 ])
	lpx =OX (px [x -1 ,y ])
	rpx =OX (px [x +1 ,y ])
	cpx =OX (px [x ,y ])
	if 1 <(tpx +bpx +lpx +rpx +cpx )<5 :
		if px [x ,y ]:
			px2 [x ,y ]=0
		else :
			px2 [x ,y ]=255
def roughimg (im ,level ,savename =None ):
	if level ==0 :
		im2 =im
	elif level >0 :
		im2 =im .copy ()
		mx ,my =im .size
		mx2 =mx -2
		px =im .load ()
		px2 =im2 .load ()
		hashtuple =gethashtuple (im )
		for y in range (1 ,my -1 ):
			for x in range (1 ,mx -1 ):
				pxset (px ,px2 ,x ,y ,hashtuple ,mx2 ,level )
	if savename :
		im2 .save (savename )
	return im2
