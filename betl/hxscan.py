from PIL import Image
from binkeul .betl .hxplot import HxPlotFrm
from binkeul .betl .hx import Hx ,HxSet
class HxScanFrm (HxPlotFrm ):
	uniqobj =None
	def __new__ (cls ):
		if cls .uniqobj :
			return cls .uniqobj
		cls .uniqobj =super ().__new__ (cls )
		return cls .uniqobj
	def __init__ (self ):
		super ().__init__ (unitsize =1 )
	def _count_black (self ,im ,*ptxys ):
		cnt =0
		for px in map (im .getpixel ,ptxys ):
			if px ==0 :cnt +=1
		return cnt
	def _PT_count_black (self ,im ,u ,v ):
		x ,y =self .gridPT (u ,v )
		return self ._count_black (im ,(x ,y ),(x +1 ,y ),(x ,y +1 ),(x +1 ,y +1 ))
	def readP (self ,im ,u ,v ,hxset ):
		bcnt =self ._PT_count_black (im ,u ,v )
		if bcnt ==4 :
			hxset .add (Hx (u ,v ,'P'))
	def readT (self ,im ,u ,v ,hxset ):
		bcnt =self ._PT_count_black (im ,u ,v )
		assert bcnt in (0 ,2 ,4 ),"uv : {},{}".format (u ,v )
		if bcnt ==4 :
			hxset .add (Hx (u ,v ,'T'))
	def readR (self ,im ,u ,v ,hxset ):
		x ,y =self .gridRL (u ,v )
		bcnt =self ._count_black (im ,(x ,y ),(x +1 ,y +1 ),(x +2 ,y +2 ),(x +3 ,y +3 ))
		if bcnt ==4 :
			hxset .add (Hx (u ,v ,'R'))
	def readL (self ,im ,u ,v ,hxset ):
		x ,y =self .gridRL (u ,v )
		bcnt =self ._count_black (im ,(x ,y +3 ),(x +1 ,y +2 ),(x +2 ,y +1 ),(x +3 ,y ))
		if bcnt ==4 :
			hxset .add (Hx (u ,v ,'L'))
	def read (self ,im ,imcmp =True ):
		im =im .convert ('1')
		hxset =HxSet ()
		wh =self .unitsize *2
		i =0
		for v in range (-4 ,5 ):
			for u in range (-4 ,5 ):
				i +=1
				if (u *v )%2 :
					i +=1
					self .readL (im ,u ,v ,hxset )
					self .readR (im ,u ,v ,hxset )
				elif (u +v )%2 :
					self .readT (im ,u ,v ,hxset )
				else :
					self .readP (im ,u ,v ,hxset )
		if imcmp :
			assert self .cmp_img_uvk (im ,hxset )==True
		return hxset
	def cmp_img_uvk (self ,im ,hxset ):
		return im .tobytes ()==self .draw (hxset ).tobytes ()
HxScanner =HxScanFrm ()
def hxScan (im ):
	if type (im )==str :
		im =Image .open (im )
	return HxScanner .read (im )
