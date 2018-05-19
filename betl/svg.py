from binkeul .betl .hx import Hx ,HxSet
from binkeul .betl .keul import Keul
from binkeul .betl .bkode import BKode
from binkeul .betl .ukode import UKode
from binkeul .betl .solnode import SKode
from binkeul .betl .hxpath import HxPath
from binkeul .betl .pubcls import Po ,Rect ,Sz ,SizeStyle ,FixStyle ,FixR
from binkeul .base import CONF ,SVGCONF
from functools import lru_cache
import copy
import svgwrite
import re
DefaultScale =2
class SvgElem ():
	def __init__ (self ,kode ,conf ):
		self .kode =kode
		self .conf =conf
		self .id =kode .toZ3a2s ()
		if type (self .kode )in (BKode ,SKode ):
			self .rect =self .kode .rect
		elif type (self .kode )in (UKode ,):
			self .rect =self .kode .getRect (self .conf ["ukode-size-style"])
		self .svg =None
	def move (self ):
		raise NotImplementedError
	def __str__ (self ):
		return self .svg .tostring ()
class SvgUse (SvgElem ):
	def __init__ (self ,kode ,conf ):
		super ().__init__ (kode ,conf )
		self .svg =svgwrite .container .Use (href ="#"+self .id )
	def move (self ,x ,y ):
		self .svg ['x']=x
		self .svg ['y']=y
		return self
class SvgItem (SvgElem ):
	def __init__ (self ,kode ,conf ,usedefs =False ,b64img =False ):
		super ().__init__ (kode ,conf )
		if type (kode )in (BKode ,SKode ):
			hxs =kode .getHxs ()
			hxp =HxPath (hxs )
			self .svg =svgwrite .path .Path (d =hxp .getPathd (simple =True ))
			self .trsform =lambda x ,y :"translate({},{}) skewX(-5)".format (x ,y )
		elif type (kode )in (UKode ,):
			self .svg =svgwrite .image .Image (
			href =kode .getDataB64 ()if b64img else kode .getUrl (),
			size =self .rect .size )
			self .trsform =lambda x ,y :"translate({},{})".format (x +self .rect .left ,y +self .rect .top )
		else :
			raise ValueError
		if usedefs :
			self .svg ["id"]=self .id
		self .move (0 ,0 )
	def move (self ,x ,y ):
		self .svg ["transform"]=self .trsform (x ,y )
		return self
mgRect =lambda rt ,mg :Rect (
rt .left -mg .w ,
rt .top -mg .h ,
rt .right +mg .w ,
rt .bottom +mg .h ,
)
class SvgLayout ():
	def __init__ (self ,space =Sz (1 ,1 ),margin =Sz (3 ,1 ),hor =True ,limit =0 ,usedefs =False ,conf ={}):
		super ().__init__ ()
		self .space =space
		self .margin =margin
		self .hor =hor
		self .limit =limit
		self .conf =CONF .chainmap (conf )
		self .usedefs =usedefs
		self .reset ()
	def reset (self ):
		self .items =None
		self .inpos =None
		self .rect =None
		self .defs =None
	def getDefs (self ):
		return self .defs
	def setDefs (self ,items ):
		self .defs =[]
		if self .usedefs :
			for kode in set (items ):
				self .defs .append (SvgItem (kode ,conf =self .conf ,usedefs =True ))
	def setItems (self ,items ):
		raise NotImplementedError ()
	def getItems (self ):
		return map (
		lambda po ,item :item .move (*po ),
		self .inpos ,self .items )
class SvgLineLayout (SvgLayout ):
	def setItems (self ,keul ):
		self .reset ()
		self .setDefs (keul )
		sp =self .space
		keul =Keul (copy .deepcopy (keul ))
		curpo =Po (0 ,0 )
		while keul :
			rect ,inpos ,items =self .lineByKeul (keul )
			if self .rect ==None :
				self .rect =rect
				self .inpos =inpos
				self .items =items
			else :
				if self .hor :
					self .rect .right =max (self .rect .right ,rect .right )
					curpo =Po (0 ,self .rect .bottom +sp .h -rect .top )
					self .rect .bottom +=sp .h +rect .height
				else :
					self .rect .bottom =max (self .rect .bottom ,rect .bottom )
					curpo =Po (self .rect .right +sp .w -rect .left ,0 )
					self .rect .right +=sp .w +rect .width
				inpos =list (Po (curpo .x +po .x ,curpo .y +po .y )for po in inpos )
				self .inpos .extend (inpos )
				self .items .extend (items )
		self .rect =mgRect (self .rect ,self .margin )
	def lineByKeul (self ,keul ):
		sp =self .space
		mg =Sz (0 ,0 )
		limit =self .limit
		items =[]
		inpos =[]
		minlt =-FixR
		maxrb =FixR
		prepo =Po (0 ,0 )
		while len (keul ):
			kode =keul [0 ]
			if self .usedefs :
				item =SvgUse (kode ,conf =self .conf )
			else :
				item =SvgItem (kode ,usedefs =False ,conf =self .conf )
			rect =item .rect
			if self .hor :
				inpo =Po (prepo .x -rect .left ,prepo .y )
				curpo =Po (prepo .x +rect .width +sp .w ,prepo .y )
				minlt =min (minlt ,rect .top )
				maxrb =max (maxrb ,rect .bottom )
				if limit and curpo .x >limit :break
			else :
				inpo =Po (prepo .x ,prepo .y -rect .top )
				curpo =Po (prepo .x ,prepo .y +rect .height +sp .h )
				minlt =min (minlt ,rect .left )
				maxrb =max (maxrb ,rect .right )
				if limit and curpo .y >limit :break
			prepo =curpo
			keul .pop (0 )
			inpos .append (inpo )
			items .append (item )
		if self .hor :
			rect =Rect (-mg .w ,minlt -mg .h ,mg .w +prepo .x -sp .w ,maxrb +mg .h )
		else :
			rect =Rect (minlt -mg .w ,-mg .h ,maxrb +mg .w ,mg .h +prepo .y -sp .h )
		return rect ,inpos ,items
class KeulSvgFrm ():
	def __init__ (self ,layout =None ,scale =DefaultScale ,usedefs =None ,svgconf ={}):
		if layout ==None :
			self .layout =SvgLineLayout ()
		else :
			self .layout =layout
		self .scale =scale
		self .svgconf =SVGCONF .chainmap (svgconf )
	def make (self ,keul ,file =None ):
		self .layout .setItems (keul )
		rt =self .layout .rect
		size =(rt .width *self .scale ,rt .height *self .scale )
		dwg =svgwrite .Drawing (size =size ,viewBox ="{} {} {} {}".format (rt .left ,rt .top ,rt .width ,rt .height ))
		defs =svgwrite .container .Defs ()
		for item in self .layout .getDefs ():
			defs .add (item .svg )
		dwg .add (defs )
		g =dwg .g (**self .svgconf )
		for item in self .layout .getItems ():
			g .add (item .svg )
		dwg .add (g )
		if file :
			with open (file ,'w')as f :
				f .write (dwg .tostring ())
		else :
			return bytes (dwg .tostring (),"ascii")
class KodeSvgFrm ():
	def __init__ (self ,scale =DefaultScale ,fix =FixStyle .square ,margin =Sz (1 ,1 ),b64img =True ,svgconf ={}):
		self .fix =fix
		self .margin =margin
		self .scale =scale
		self .b64img =b64img
		self .svgconf =SVGCONF .chainmap (svgconf )
	def draw (self ,kode ,file =None ):
		conf ={"ukode-size-style":SizeStyle .pic1x }
		item =SvgItem (kode ,conf =conf ,b64img =self .b64img )
		mg =self .margin
		rt =item .rect .fixRect (self .fix )
		rt =mgRect (rt ,mg )
		size =(rt .width *self .scale ,rt .height *self .scale )
		dwg =svgwrite .Drawing (size =size ,viewBox ="{} {} {} {}".format (rt .left ,rt .top ,rt .width ,rt .height ))
		g =dwg .g (**self .svgconf )
		g .add (item .svg )
		dwg .add (g )
		if file :
			with open (file ,'w')as f :
				f .write (dwg .tostring ())
		else :
			return bytes (dwg .tostring (),'ascii')
from binkeul .base import fCached
class KodeSvgFrmForQt (KodeSvgFrm ):
	boxinfo =b'''height="44" version="1.1" viewBox="-11 -11 22 22" width="44"'''
	def __init__ (self ,drawfix ):
		super ().__init__ (scale =DefaultScale ,fix =FixStyle .square ,margin =Sz (1 ,1 ),b64img =True )
		self .drawfix =drawfix
	def replaceUKodeSvg (self ,ukode ):
		mainsvg =ukode .getData ()[0 ]
		mg =self .margin
		rt =ukode .rect .fixRect (self .drawfix )
		rt =mgRect (rt ,mg )
		w ,h =rt .size
		mainsvg =re .sub (b'''width=\"[^"]+\"''',b'''width="%d"'''%w ,mainsvg ,1 )
		mainsvg =re .sub (b'''height=\"[^"]+\"''',b'''height="%d"'''%h ,mainsvg ,1 )
		return mainsvg
	@fCached ()
	def draw (self ,kode ):
		if isinstance (kode ,UKode )and kode .get ('kind')==".svg":
			return self .replaceUKodeSvg (kode )
		if self .drawfix ==FixStyle .square :
			return self .__draw (kode )
		if kode .rect ==Rect (-10 ,-10 ,10 ,10 ):
			return self .__draw (kode )
		mg =self .margin
		rt =kode .rect .fixRect (self .drawfix )
		rt =mgRect (rt ,mg )
		size =(rt .width *self .scale ,rt .height *self .scale )
		repl_boxinfo =b'''width="%d" height="%d" version="1.1" viewBox="%d %d %d %d" '''%(
		rt .width *self .scale ,
		rt .height *self .scale ,
		rt .left ,
		rt .top ,
		rt .width ,
		rt .height
		)
		outsvg =self .__draw (kode )
		outsvg =outsvg .replace (self .boxinfo ,repl_boxinfo ,1 )
		return outsvg
	def __draw (self ,kode ):
		return super ().draw (kode ,False )
	def __repr__ (self ):
		return "KodeSvgFrmForQt({})".format (self .drawfix )
