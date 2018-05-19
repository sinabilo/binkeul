import random ,pdb ,collections ,enum
from PySide import QtCore ,QtGui
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .qkpub import QkKodeSize
from binkeul .qkui .butlab import QkIcon ,QkLabel
from binkeul .betl .keul import Keul
from binkeul .betl .kode import Kode
from binkeul .betl .pubcls import FixStyle
from binkeul import at_end
class QkListModel (QAbstractListModel ):
	def __init__ (self ,kodes ,parent =None ):
		super ().__init__ (parent )
		self .kodes =kodes
	def rowCount (self ,index ):
		return len (self .kodes )
	def data (self ,index ,role ):
		if not index .isValid ()or not (0 <=index .row ()<len (self .kodes )):return QtCore .QVariant ()
		kode =self .kodes [index .row ()]
		if role ==Qt .DisplayRole :
			return ""
		elif role ==Qt .DecorationRole :
			return QIcon (QkIcon (kode ))
		elif role ==Qt .ToolTipRole :
			return kode .toZ3a2s ()
class QkListView (QListView ):
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
		''''''
		self .setKodes (kodes )
		self .clicked .connect (self .pick_kode )
		self .doubleClicked .connect (self .ppick_kode )
	def setKodes (self ,kodes ):
		model =QkListModel (kodes [:self .limit ])
		self .setModel (model )
	def wheelEvent (self ,event ):
		super ().wheelEvent (event )
		if self .flow ()==QListView .TopToBottom :
			self .horizontalScrollBar ().wheelEvent (event )
			self .verticalScrollBar ().setValue (0 )
		else :
			self .verticalScrollBar ().wheelEvent (event )
			self .horizontalScrollBar ().setValue (0 )
	def kode (self ,idx ):
		return self .model ().kodes [idx .row ()]
	def pick_kode (self ,idx ):
		self .sg_pick_kode .emit (self .kode (idx ))
	def ppick_kode (self ,idx ):
		self .sg_ppick_kode .emit (self .kode (idx ))
