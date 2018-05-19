import random ,pdb ,collections ,enum
from PySide import QtCore ,QtGui
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .qkpub import QkKodeSize
from binkeul .qkui .butlab import QkIcon ,QkLabel ,QkWLabel ,QkWButton
from binkeul .betl .keul import Keul
from binkeul .betl .kode import Kode
from binkeul .betl .pubcls import FixStyle
class QkWListWgt (QListWidget ):
	sg_pick_keul =Signal (Keul )
	sg_ppick_keul =Signal (Keul )
	def __init__ (self ,
	keuls =[],
	fix =FixStyle .hor ,
	direction =Qt .RightToLeft ,
	limit =50 ,
	parent =None ):
		super ().__init__ (parent )
		self .limit =limit
		self .setKeuls (keuls )
		self .setIconSize (QkKodeSize )
		self .setResizeMode (QListView .Adjust )
		self .setWrapping (True )
		self .setFocusPolicy (Qt .WheelFocus )
		self .setLayoutDirection (direction )
		self .fix =fix
		if self .fix ==FixStyle .hor :
			self .setFlow (QListView .LeftToRight )
		else :
			self .setFlow (QListView .TopToBottom )
		self .clicked .connect (self .pick_keul )
		self .doubleClicked .connect (self .ppick_keul )
	def setKeuls (self ,keuls ):
		self .clear ()
		self .keuls =list (keuls )[:self .limit ]
		for keul in keuls :
			item =QListWidgetItem ()
			i =self .addItem (item )
			wgt =QkWLabel (keul ,self .fix )
			item .setSizeHint (wgt .sizeHint ())
			self .setItemWidget (item ,wgt )
	def keul (self ,idx ):
		return self .keuls [idx .row ()]
	def pick_keul (self ,idx ):
		self .sg_pick_keul .emit (self .keul (idx ))
	def ppick_keul (self ,idx ):
		self .sg_ppick_keul .emit (self .keul (idx ))
class QkListWgt (QListWidget ):
	sg_pick_kode =Signal (Kode )
	sg_ppick_kode =Signal (Kode )
	def __init__ (self ,
	kodes =[],
	flow =QListView .TopToBottom ,
	direction =Qt .RightToLeft ,
	limit =100 ,
	parent =None ):
		super ().__init__ (parent )
		self .limit =limit
		self .setWrapping (True )
		self .setIconSize (QkKodeSize )
		self .setFlow (flow )
		self .setResizeMode (QListView .Adjust )
		self .setViewMode (QListView .ListMode )
		self .setFocusPolicy (Qt .WheelFocus )
		self .setLayoutDirection (direction )
		self .setSelectionMode (QAbstractItemView .ExtendedSelection )
		self .setKodes (kodes )
		self .clicked .connect (self .pick_kode )
		self .doubleClicked .connect (self .ppick_kode )
	def setKodes (self ,kodes ):
		self .clear ()
		self .kodes =kodes [:self .limit ]
		for kode in kodes :
			item =QListWidgetItem (QkIcon (kode ),"")
			i =self .addItem (item )
		if len (self .kodes ):
			self .setCurrentRow (0 )
	def wheelEvent (self ,event ):
		super ().wheelEvent (event )
		if self .flow ()==QListView .TopToBottom :
			self .horizontalScrollBar ().wheelEvent (event )
			self .verticalScrollBar ().setValue (0 )
		else :
			self .verticalScrollBar ().wheelEvent (event )
			self .horizontalScrollBar ().setValue (0 )
	def kode (self ,idx ):
		return self .kodes [idx .row ()]
	def pick_kode (self ,idx ):
		self .sg_pick_kode .emit (self .kode (idx ))
	def ppick_kode (self ,idx ):
		self .sg_ppick_kode .emit (self .kode (idx ))
