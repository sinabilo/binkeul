from binkeul .betl .pubcls import FixStyle ,Sz ,FixR
from binkeul .betl .bkode import BKode
from binkeul .betl .ukode import UKode
from binkeul .betl .solnode import SKode
from binkeul .at_end import pCached
from binkeul .betl .hxplot import HxPlotFrm
from binkeul .tools import pilfunc
from PySide .QtCore import QByteArray ,QBuffer ,QIODevice
from PySide .QtGui import QPixmap ,QPixmapCache
from collections import namedtuple
from functools import lru_cache
class KodeMapCache (QPixmapCache ):
	_dic ={}
	def __new__ (cls ,unitsize =2 ,fix =FixStyle .square ):
		key =(unitsize ,fix )
		if key in cls ._dic :
			return cls ._dic [key ]
		else :
			obj =super ().__new__ (cls )
			return obj
	def __init__ (self ,unitsize =2 ,fix =FixStyle .square ):
		key =(unitsize ,fix )
		if key in self ._dic :
			return
		else :
			self ._dic [key ]=self
			super ().__init__ ()
class KodeMapFrm (namedtuple ("_KodeMapFrm",["unitsize","fix"])):
	def __new__ (cls ,unitsize ,fix ):
		return super ().__new__ (cls ,unitsize ,fix )
	def __init__ (self ,unitsize ,fix ):
		self .plotter =HxPlotFrm (unitsize =unitsize ,fix =fix )
	def draw (self ,kode ):
		if isinstance (kode ,UKode ):
			return kode .getThumb (self .unitsize ,self .fix )
		elif isinstance (kode ,(BKode ,SKode )):
			im =self .plotter .draw (kode .getHxs ())
			im =im .convert ('RGBA')
			im =pilfunc .set_alpha (im )
			return im
		else :
			raise ValueError ('kode 의 타입은 UKode, BKode, SKode 에 속해야 함')
	@property
	def maxsz (self ):
		return self .unitsize *FixR *2
	@pCached ()
	def mapSize (self ,kode ):
		r =kode .rect .fixRect (self .fix ).scRect (self .unitsize )
		return Sz (r .width ,r .height )
	@pCached ()
	def mapBytes (self ,kode ):
		im =self .draw (kode )
		if isinstance (kode ,UKode ):
			qxm =pilfunc .pixmap2qt (im )
		elif isinstance (kode ,(BKode ,SKode )):
			qxm =pilfunc .bitmap2qt (im )
		else :
			raise ValueError
		bts =QByteArray ()
		buffer =QBuffer (bts )
		buffer .open (QIODevice .WriteOnly )
		qxm .save (buffer ,"png")
		buffer .close ()
		return bts
	def getMap (self ,kode ,kmapCache ,bkode_bg =False ):
		key =kode .toZ3a2s ()+"-{}-{}".format (self .unitsize ,self .fix .value )
		pixmap =kmapCache .find (key )
		if pixmap :return pixmap
		pixmap =QPixmap ()
		pixmap .loadFromData (self .mapBytes (kode ))
		if not (bkode_bg )and isinstance (kode ,(BKode ,SKode )):
			pixmap .setMask (pixmap )
		kmapCache .insert (key ,pixmap )
		return pixmap
