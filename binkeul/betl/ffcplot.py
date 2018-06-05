'''
'''
from PIL import Image ,ImageOps ,ImageDraw
from binkeul .betl .pubcls import FixStyle
from binkeul .betl .ffc import FfcSet
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
		wsz =self .unitsize *12
		hsz =self .unitsize *20
		return Image .new ('1',(wsz ,hsz ),color =1 )
	def unitmap (self ,unitsize =1 ):
		uz =unitsize
		self .D =Image .new ('1',(uz *2 ,uz *2 ),0 )
class FfcPlotFrm :
	def __init__ (self ,unitsize =2 ,fix =FixStyle .hor ):
		'''
        '''
		self .um =_Unitmap (unitsize )
		self .fix =FixStyle .hor if fix ==FixStyle .square else fix
	def __repr__ (self ):
		return "HxPlotFrm({},{})".format (self .um .unitsize ,self .fix )
	@property
	def unitsize (self ):
		return self .um .unitsize
	def grid (self ,u ,v ,ofsx ,ofsy ):
		uz =self .unitsize
		assert abs (u )<3 and abs (v )<5
		cen_x =uz *6
		cen_y =uz *10
		ru =cen_x +u *uz *2 +ofsx
		rv =cen_y +v *uz *2 +ofsy
		return (ru ,rv )
	def gridD (self ,u ,v ):
		ofs =-self .unitsize
		return self .grid (u ,v ,ofs ,ofs )
	pasteD =lambda self ,im ,u ,v :im .paste (self .um .D ,self .gridD (u ,v ))
	def draw (self ,ffcset ):
		im =self .um .newmap ()
		assert isinstance (ffcset ,FfcSet )
		for u ,v in ffcset .gen ():
			self .pasteD (im ,u ,v )
		if self .fix ==FixStyle .ver :
			return im .transpose (Image .ROTATE_270 )
		else :
			return im
