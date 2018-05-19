from PIL import Image ,ImageOps ,ImageDraw
import io
from binkeul .betl .hx import HxSet
from binkeul .betl .pubcls import Rect ,Po ,FixStyle ,FixR
class _Unitmap :
	_dic ={}
	def __new__ (cls ,unitsize =2 ):
		if unitsize in cls ._dic :
			return cls ._dic [unitsize ]
		cls ._dic [unitsize ]=super ().__new__ (cls )
		return cls ._dic [unitsize ]
	def __init__ (self ,unitsize =2 ):
		self .unitmap (unitsize )
		self .unitsize =unitsize
		pass
	def newmap (self ):
		whsz =self .unitsize *20
		return Image .new ('1',(whsz ,whsz ),color =1 )
	def unitmap (self ,unitsize =1 ):
		uz =unitsize
		self .PT =Image .new ('1',(uz *2 ,uz *2 ),0 )
		if uz >2 :
			self .WdotP =Image .new ('1',(uz *2 ,uz *2 ),0 )
			wdot_draw =ImageDraw .Draw (self .WdotP )
			wdot_draw .rectangle ((uz -1 ,uz -1 ,uz ,uz ),fill =255 )
		else :
			self .WdotP =self .PT
		self .R =Image .new ('1',(uz *4 ,uz *4 ),255 )
		self .L =Image .new ('1',(uz *4 ,uz *4 ),255 )
		umlrx =Image .new ('1',(uz ,uz ),0 )
		lrpxnum =self .L .size [0 ]-(uz -1 )
		lmax =self .L .size [0 ]-uz
		for x in range (lrpxnum ):
			self .R .paste (umlrx ,(x ,x ))
		for x in range (lrpxnum ):
			self .L .paste (umlrx ,(lmax -x ,x ))
		self .Li =ImageOps .invert (self .L .convert ('L'))
		self .Ri =ImageOps .invert (self .R .convert ('L'))
class HxPlotFrm :
	def __init__ (self ,unitsize =2 ,fix =FixStyle .square ):
		self .um =_Unitmap (unitsize )
		self .fix =fix
	def __repr__ (self ):
		return "HxPlotFrm({},{})".format (self .um .unitsize ,self .fix )
	@property
	def unitsize (self ):
		return self .um .unitsize
	def grid (self ,u ,v ,ofsx ,ofsy ):
		uz =self .unitsize
		assert abs (u )<5 and abs (v )<5
		cen_x =cen_y =uz *10
		ru =cen_x +u *uz *2 +ofsx
		rv =cen_y +v *uz *2 +ofsy
		return (ru ,rv )
	def gridPT (self ,u ,v ):
		ofs =-self .unitsize
		return self .grid (u ,v ,ofs ,ofs )
	def gridRL (self ,u ,v ):
		ofs =-(self .unitsize *2 )
		return self .grid (u ,v ,ofs ,ofs )
	pasteWdotP =lambda self ,im ,u ,v :im .paste (self .um .WdotP ,self .gridPT (u ,v ))
	pastePT =lambda self ,im ,u ,v :im .paste (self .um .PT ,self .gridPT (u ,v ))
	pasteR =lambda self ,im ,u ,v :im .paste (self .um .R ,self .gridRL (u ,v ),self .um .Ri )
	pasteL =lambda self ,im ,u ,v :im .paste (self .um .L ,self .gridRL (u ,v ),self .um .Li )
	def draw (self ,hxset ,wdot =False ):
		im =self .um .newmap ()
		assert isinstance (hxset ,HxSet )
		for hx in hxset .gen ():
			u ,v ,k ,_ =hx .gettuple ()
			if k in 'PT':self .pastePT (im ,u ,v )
			elif k =='R':self .pasteR (im ,u ,v )
			elif k =='L':self .pasteL (im ,u ,v )
		if wdot :
			for hx in hxset :
				u ,v ,k ,_ =hx .gettuple ()
				if k !='P':continue
				self .pasteWdotP (im ,u ,v )
		return self ._fixImage (hxset ,im )
	def _fixImage (self ,hxset ,im ):
		if self .fix ==FixStyle .square :
			return im
		rt =hxset .rect
		croprt =rt .fixRect (self .fix ,-FixR ,FixR ).mvRect (Po (FixR ,FixR )).scRect (self .um .unitsize )
		return im .crop (tuple (croprt ))
HxPlotter =HxPlotFrm (1 )
def hxPrint (hxs ):
	im =HxPlotter .draw (hxs )
	print ("[")
	for i ,px in enumerate (im .getdata ()):
		if i and not (i %20 ):
			print ()
		print (px ,end =",")
	print ("]")
def hxPrint2 (hxs ):
	im =HxPlotter .draw (hxs )
	for i ,px in enumerate (im .getdata ()):
		if i and not (i %20 ):
			print ()
		print ("0"if px ==0 else " ",end =" ")
def hxPlot (unitsize ,hxs ,outfile =None ):
	plotter =HxPlotFrm (unitsize )
	im =plotter .draw (hxs )
	return im
if __name__ =="""__main__""":
	import argparse
	parser =argparse .ArgumentParser (description ='20x20  40x40 ... 빈글문자의 흑백이미지를 그린다. ')
	parser .add_argument ('hxset',metavar ='H',type =int ,nargs ="*",help ='hxset')
	parser .add_argument ('-b','--bitset',type =str ,help ='1 0 bitset',default ="0")
	parser .add_argument ('-o','--outfile',type =str ,help ='btmap file')
	parser .add_argument ('-u','--unitsize',type =int ,help ='pixel unitsize',default =1 )
	args =parser .parse_args ()
	def main (args ):
		hxs =HxSet ("{:0>97}".format (args .bitset ))
		hxs .update (args .hxset )
		hxPrint (hxs )
		if args .outfile :
			plotter =HxPlotFrm (args .unitsize )
			im =plotter .draw (hxs )
			im .save (args .outfile )
	main (args )
