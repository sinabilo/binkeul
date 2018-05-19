import random ,pdb ,collections ,enum
from PySide import QtCore ,QtGui
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .qkpub import QkKodeSize ,QkKodeHeight
from binkeul .qkui .kodemap import KodeMapCache ,KodeMapFrm
from binkeul .betl .keul import Keul
from binkeul .betl .hx import HxSet
from binkeul .betl .pubcls import FixStyle
from binkeul .betl .hxplot import HxPlotFrm
from binkeul .tools import pilfunc
from binkeul import at_end
kmapCache =KodeMapCache (2 ,FixStyle .square )
kmapCache_hor =KodeMapCache (2 ,FixStyle .hor )
kmapCache_ver =KodeMapCache (2 ,FixStyle .ver )
kmapEng =KodeMapFrm (2 ,FixStyle .square )
kmapEng_hor =KodeMapFrm (2 ,FixStyle .hor )
kmapEng_ver =KodeMapFrm (2 ,FixStyle .ver )
class QFlowLayout (QtGui .QLayout ):
	def __init__ (self ,parent =None ,margin =0 ,spacing =-1 ):
		super ().__init__ (parent )
		if parent is not None :
			self .setMargin (margin )
		self .setSpacing (spacing )
		self .itemList =[]
	def __del__ (self ):
		item =self .takeAt (0 )
		while item :
			item =self .takeAt (0 )
	def addItem (self ,item ):
		self .itemList .append (item )
	def count (self ):
		return len (self .itemList )
	def itemAt (self ,index ):
		if index >=0 and index <len (self .itemList ):
			return self .itemList [index ]
		return None
	def takeAt (self ,index ):
		if index >=0 and index <len (self .itemList ):
			return self .itemList .pop (index )
		return None
	def expandingDirections (self ):
		return QtCore .Qt .Orientations (QtCore .Qt .Orientation (0 ))
	def hasHeightForWidth (self ):
		return True
	def heightForWidth (self ,width ):
		height =self .doLayout (QtCore .QRect (0 ,0 ,width ,0 ),True )
		return height
	def setGeometry (self ,rect ):
		super ().setGeometry (rect )
		self .doLayout (rect ,False )
	def sizeHint (self ):
		return self .minimumSize ()
	def minimumSize (self ):
		size =QtCore .QSize ()
		for item in self .itemList :
			size =size .expandedTo (item .minimumSize ())
		size +=QtCore .QSize (2 *self .contentsMargins ().top (),2 *self .contentsMargins ().top ())
		return size
	def doLayout (self ,rect ,testOnly ):
		x =rect .x ()
		y =rect .y ()
		lineHeight =0
		for item in self .itemList :
			wid =item .widget ()
			spaceX =self .spacing ()+wid .style ().layoutSpacing (QtGui .QSizePolicy .PushButton ,QtGui .QSizePolicy .PushButton ,QtCore .Qt .Horizontal )
			spaceY =self .spacing ()+wid .style ().layoutSpacing (QtGui .QSizePolicy .PushButton ,QtGui .QSizePolicy .PushButton ,QtCore .Qt .Vertical )
			nextX =x +item .sizeHint ().width ()+spaceX
			if nextX -spaceX >rect .right ()and lineHeight >0 :
				x =rect .x ()
				y =y +lineHeight +spaceY
				nextX =x +item .sizeHint ().width ()+spaceX
				lineHeight =0
			if not testOnly :
				item .setGeometry (QtCore .QRect (QtCore .QPoint (x ,y ),item .sizeHint ()))
			x =nextX
			lineHeight =max (lineHeight ,item .sizeHint ().height ())
		return y +lineHeight -rect .y ()
class QkIcon (QIcon ):
	def __init__ (self ,kode ):
		self .kode =kode
		pixmap =kmapEng .getMap (kode ,kmapCache )
		super ().__init__ (pixmap )
class QkButton (QPushButton ):
	def __init__ (self ,kode ,cha ='',parent =None ):
		self .kode =kode
		text =kode .toZ3a2s ()
		icon =QkIcon (kode )
		super ().__init__ (icon ,cha ,parent )
		self .setIconSize (QkKodeSize )
		self .setMinimumHeight (QkKodeHeight )
		self .clicked .connect (self .prt )
		self .setStyleSheet ('''background-color:#FFFFFF;color:#000000;
        border-width: 5px;
        ''')
	def prt (self ):
		print (self .text (),repr (self .kode ))
class QkBLabel (QLabel ):
	'''DB 에 등록되지 않은 BKode를 직접 그릴 때 사용한다. setKodeDlg 에서 사용'''
	def __init__ (self ,hxset =HxSet (),unitsize =2 ,fix =FixStyle .square ,parent =None ):
		self .plotter =HxPlotFrm (unitsize ,fix )
		super ().__init__ (parent )
		self .setHxs (hxset )
		self .setAlignment (Qt .AlignHCenter |Qt .AlignVCenter );
		self .setContentsMargins (0 ,0 ,0 ,0 )
		self .setFrameStyle (QFrame .Box |QFrame .Raised )
		self .setLineWidth (2 )
	def setHxs (self ,hxset ):
		im =self .plotter .draw (hxset )
		pixmap =pilfunc .bitmap2qt (im )
		pixmap .setMask (pixmap )
		self .setPixmap (pixmap )
class QkLabel (QLabel ):
	def __init__ (self ,kode ,fix =FixStyle .hor ,parent =None ):
		self .kode =kode
		if fix ==FixStyle .hor :
			self .mapeng =kmapEng_hor
			self .mapcache =kmapCache_hor
		elif fix ==FixStyle .ver :
			self .mapeng =kmapEng_ver
			self .mapcache =kmapCache_ver
		else :
			raise ValueError
		super ().__init__ (parent )
		self .setPixmap (self .mapeng .getMap (kode ,self .mapcache ,False ))
		self .setContentsMargins (0 ,0 ,0 ,0 )
class QkWLabel (QFrame ):
	def __init__ (self ,kodes ,fix =FixStyle .hor ,parent =None ):
		super ().__init__ (parent )
		assert fix in (FixStyle .hor ,FixStyle .ver )
		self .kodes =kodes
		self .setContentsMargins (0 ,0 ,0 ,0 )
		if fix ==FixStyle .hor :
			lay =QHBoxLayout ()
			lay .setContentsMargins (5 ,0 ,5 ,0 )
		elif fix ==FixStyle .ver :
			lay =QVBoxLayout ()
			lay .setContentsMargins (0 ,5 ,0 ,5 )
		self .setSizePolicy (QSizePolicy .Fixed ,QSizePolicy .Fixed )
		for kode in kodes :
			lb =QkLabel (kode ,fix )
			lay .addWidget (lb )
		lay .addStretch (0 )
		lay .setSpacing (0 )
		self .setLayout (lay )
class QkWButton (QkWLabel ):
	def __init__ (self ,kodes ,fix =FixStyle .hor ,parent =None ):
		super ().__init__ (kodes ,fix ,parent =parent )
		self .setFrm (True )
	def setFrm (self ,up =True ):
		if up :
			self .setFrameShadow (QFrame .Raised )
			self .setFrameStyle (QFrame .Panel |QFrame .Raised )
			self .setLineWidth (2 )
		else :
			self .setFrameStyle (QFrame .Panel |QFrame .Sunken )
			self .setLineWidth (2 )
	def mousePressEvent (self ,e ):
		self .setFrm (False )
	def mouseReleaseEvent (self ,e ):
		self .setFrm (True )
