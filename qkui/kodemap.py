'''
Kode 의 비트맵이미지를 그린다.  QImage, QPixmap 를 만들기 위해 사용된다.
qkui/qkmap 에서 사용한다.
'''
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
	''' 생성 매개변수에 따라 고유한 객체만이 생성되도록 한다.
    '''
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
	'''문자이미지를 위한 QPixmap 을 생성한다.
    '''
	def __new__ (cls ,unitsize ,fix ):
		return super ().__new__ (cls ,unitsize ,fix )
	def __init__ (self ,unitsize ,fix ):
		self .plotter =HxPlotFrm (unitsize =unitsize ,fix =fix )
	def draw (self ,kode ):
		'''문자 이미지 (PIL.Image) 생성 '''
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
		"""가로 또는 세로의 최대길이"""
		return self .unitsize *FixR *2
	@pCached ()
	def mapSize (self ,kode ):
		"문자 이미지의 사이즈"
		r =kode .rect .fixRect (self .fix ).scRect (self .unitsize )
		return Sz (r .width ,r .height )
	@pCached ()
	def mapBytes (self ,kode ):
		''' QkKmap 에서 사용한다.
        ::
            km = KodeMapFrm()
            qxm = QPixmap()
            bts = km.mapBytes(bkode)
            qxm.loadFromData(bts)
        '''
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
		'''픽스맵을 생성하고 픽스맵캐시에 저장한다. kmapCache( QPixmapCache 객체 ) 은 Pyside 의 Gui 객체의 맴버여야 함, 즉 getMap 을 사용하려는 qobj(Q객체)는 kmapCache 를 가지고 있어야 한다. bkode_bg 는 bkode 인 경우 배경색을 하얗게 둔다.
        '''
		key =kode .toZ3a2s ()+"-{}-{}".format (self .unitsize ,self .fix .value )
		pixmap =kmapCache .find (key )
		if pixmap :return pixmap
		pixmap =QPixmap ()
		pixmap .loadFromData (self .mapBytes (kode ))
		if not (bkode_bg )and isinstance (kode ,(BKode ,SKode )):
			pixmap .setMask (pixmap )
		kmapCache .insert (key ,pixmap )
		return pixmap
