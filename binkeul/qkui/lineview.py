from PySide .QtCore import *
from PySide .QtGui import *
from PySide .QtGui import QClipboard
from binkeul .betl .ukode import UKode
from binkeul .betl .bkode import BKode
from binkeul .betl .keul import Keul
from binkeul .betl .pubcls import FixStyle
from binkeul import at_end
from binkeul .base import CONF
from binkeul .qkui .kodemap import KodeMapFrm ,KodeMapCache
import pdb ,random ,array
NEWLINE =65535
class QkLineDoc (QStandardItemModel ):
	contentsChanged =Signal ()
	def __init__ (self ,keul ,parent =None ,modified =False ):
		super (QkLineDoc ,self ).__init__ (parent )
		self .keul =keul
		self .rootItem =QModelIndex ()
		self ._modified =modified
	def isModified (self ):
		return self ._modified
	def setModified (self ,b ):
		self ._modified =b
	def columnCount (self ,parent =QModelIndex ()):
		return 1
	def rowCount (self ,parent =QModelIndex ()):
		return len (self .keul )
	def insertRows (self ,position ,kodes ,parent =QModelIndex ()):
		self .beginInsertRows (parent ,
		position ,position +len (kodes )-1 )
		self .keul [position :position ]=Keul (kodes )
		self .endInsertRows ()
		self .setModified (True )
		self .contentsChanged .emit ()
		return True
	def removeRows (self ,start ,end ,parent =QModelIndex ()):
		self .beginRemoveRows (parent ,start ,end )
		self .keul [start :end +1 ]=Keul ([])
		self .endRemoveRows ()
		self .setModified (True )
		self .contentsChanged .emit ()
		return True
	def __getitem__ (self ,i ):
		return self .keul [i ]
	def data (self ,index ,role =Qt .DisplayRole ):
		if not index .isValid ():
			return -1
		kode =self [index .row ()]
		if role ==Qt .DisplayRole :
			return kode
		elif role ==Qt .ToolTipRole :
			return kode .toZ3a2s ()
		else :
			return -1
	def flags (self ,index ):
		if not index .isValid ():
			return Qt .NoItemFlags
		return Qt .ItemIsEnabled |Qt .ItemIsSelectable |Qt .ItemIsEditable
	def headerData (self ,section ,orientation ,role ):
		return None
	def index (self ,row ,column =0 ,parent =QModelIndex ()):
		if not self .hasIndex (row ,column ,parent ):
			return QModelIndex ()
		if 0 <=row <=len (self .keul ):
			return self .createIndex (row ,column ,self .rootItem )
		else :
			return QModelIndex ()
	def parent (self ,child ):
		if not child .isValid ():
			return QModelIndex ()
		return QModelIndex ()
class QkLineDelegate (QAbstractItemDelegate ):
	def __init__ (self ,parent =None ):
		super (QkLineDelegate ,self ).__init__ (parent )
		self .kmapCache =KodeMapCache (2 ,FixStyle .hor )
		self .kmapEng =KodeMapFrm (2 ,FixStyle .hor )
	def getKmap (self ,kode ):
		return self .kmapEng .getMap (kode ,self .kmapCache )
	def paint (self ,painter ,option ,index ):
		if not index .model ():return
		kode =index .model ().data (index )
		painter .save ()
		painter .setPen (Qt .NoPen )
		painter .setBrush (QBrush (Qt .black ))
		pixmap =self .getKmap (kode )
		painter .drawPixmap (option .rect ,pixmap )
		painter .setCompositionMode (QPainter .CompositionMode_Multiply )
		if option .state &QStyle .State_Selected :
			painter .fillRect (option .rect ,option .palette .highlight ())
		painter .restore ()
	def sizeHint (self ,option ,index ):
		kode =index .model ().data (index )
		r =self .kmapEng .mapSize (kode )
		return QSize (r .w ,r .h )
class QkLineView (QAbstractItemView ):
	sel_current_change =Signal (str )
	copyAvailable =Signal (bool )
	def __init__ (self ,sample =0 ,parent =None ):
		super ().__init__ (parent )
		self .clipboard =QApplication .clipboard ()
		self .horizontalScrollBar ().setRange (0 ,0 )
		self .verticalScrollBar ().setRange (0 ,0 )
		self .hashIsDirty =False
		self .horizontalScrollBar ().setCursor (Qt .ArrowCursor )
		self .verticalScrollBar ().setCursor (Qt .ArrowCursor )
		self .setCursor (Qt .IBeamCursor )
		self .rectForRow =[]
		self .ExtraHeight =10
		if sample :
			self .initSample (sample )
		delegate =QkLineDelegate (self )
		self .setItemDelegate (delegate )
	@property
	def RowHeight (self ):
		return self .itemDelegate ().kmapEng .maxsz
	@property
	def UnitSize (self ):
		return self .itemDelegate ().kmapEng .unitsize
	def setItemDelegate (self ,dgt ):
		super ().setItemDelegate (dgt )
	def initSample (self ,cnt ):
		newModel =QkLineDoc (Keul .sample (cnt ),parent =self .parent ())
		self .setModel (newModel )
	def setModel (self ,model ):
		super (QkLineView ,self ).setModel (model )
		self .setRootIndex (self .model ().rootItem )
		self .hashIsDirty =True
	def calculateRectsIfNecessary (self ,_s =[0 ]):
		'''
        '''
		_s [0 ]+=1
		if not self .hashIsDirty :return
		ExtraWidth =0
		index0 =self .model ().index (0 ,0 ,self .rootIndex ())
		text =self .model ().data (index0 ,role =Qt .DisplayRole )
		RowHeight =self .RowHeight +self .ExtraHeight
		MaxWidth =self .viewport ().width ();
		minimumWidth =0
		x =0
		y =0
		self .rectForRow =[]
		oldtext =None
		for row in range (self .model ().rowCount (self .rootIndex ())):
			index =self .model ().index (row ,0 ,self .rootIndex ())
			text =self .model ().data (index ,role =Qt .DisplayRole )
			textWidth =self .itemDelegate ().kmapEng .mapSize (text ).w
			if not (x ==0 or (x +textWidth +ExtraWidth )<MaxWidth )or oldtext ==NEWLINE :
				y +=RowHeight
				x =0
			elif x !=0 :
				x +=ExtraWidth ;
			self .rectForRow .append (QRect (x ,y ,textWidth +ExtraWidth ,self .RowHeight ))
			if textWidth >minimumWidth :
				minimumWidth =textWidth
			x +=textWidth
			oldtext =text
		self .idealWidth =minimumWidth +ExtraWidth
		self .idealHeight =y +RowHeight
		self .hashIsDirty =False
		self .viewport ().update ()
	def edit (self ,index ,trigger ,event ):
		return False
	def visualRect (self ,index ):
		if index and index .isValid ():
			rect =self .viewportRectForRow (index .row ())
			if rect :
				return rect
		return QRect (0 ,0 ,0 ,0 )
	def viewportRectForRow (self ,row ):
		self .calculateRectsIfNecessary ()
		rect =self .rectForRow [row ]
		if not rect .isValid ():
			return rect
		return QRect (rect .x ()-self .horizontalScrollBar ().value (),
		rect .y ()-self .verticalScrollBar ().value (),
		rect .width (),rect .height ())
	def scrollTo (self ,index ,scrollhint ):
		viewRect =self .viewport ().rect ()
		itemRect =self .visualRect (index )
		if itemRect .left ()<viewRect .left ():
			self .horizontalScrollBar ().setValue (
			self .horizontalScrollBar ().value ()
			+itemRect .left ()-viewRect .left ()
			)
		elif itemRect .right ()>viewRect .right ():
			self .horizontalScrollBar ().setValue (
			self .horizontalScrollBar ().value ()
			+min (itemRect .right ()-viewRect .right (),
			itemRect .left ()-viewRect .left ())
			)
		if itemRect .top ()<viewRect .top ():
			self .verticalScrollBar ().setValue (
			self .verticalScrollBar ().value ()
			+itemRect .top ()-viewRect .top ()
			)
		elif itemRect .bottom ()>viewRect .bottom ():
			self .verticalScrollBar ().setValue (
			self .verticalScrollBar ().value ()+
			min (itemRect .bottom ()-viewRect .bottom (),
			itemRect .top ()-viewRect .top ())
			)
		self .viewport ().update ();
	def indexAt (self ,point ):
		point +=QPoint (
		self .horizontalScrollBar ().value (),
		self .verticalScrollBar ().value ()
		)
		self .calculateRectsIfNecessary ()
		for i ,r in enumerate (self .rectForRow ):
			if r .contains (point ):
				return self .model ().index (i ,0 ,self .rootIndex ())
		return QModelIndex ()
	def updateall (self ):
		self .setModel (self .model ())
	def reset (self ):
		super ().reset ()
	def dataChanged (self ,topLeft ,bottomRight ):
		self .hashIsDirty =True
		super (QkLineView ,self ).dataChanged (topLeft ,bottomRight )
	def moveCursor (self ,cursorAction ,KeyboardModifiers ):
		return QModelIndex ()
	def horizontalOffset (self ):
		return self .horizontalScrollBar ().value ()
	def verticalOffset (self ):
		return self .verticalScrollBar ().value ()
	def scrollContentsBy (self ,dx ,dy ):
		self .scrollDirtyRegion (dx ,dy )
		self .viewport ().scroll (dx ,dy )
	def selectGroup (self ):
		sm =self .selectionModel ()
		sall =[idx .row ()for idx in sm .selectedIndexes ()]
		slist =[]
		for i ,idx in enumerate (sall ):
			if (i ==0 )or (sall [i -1 ]+1 ==idx ):
				slist .append (idx )
			else :
				break
		return slist
	def selectionChanged (self ,selected ,deselected ,s =[0 ]):
		s [0 ]+=1
		if not selected .empty ():
			a =self .model ().data (selected .indexes ()[0 ])
			self .sel_current_change .emit (a .toZ3a2s ())
			self .copyAvailable .emit (True )
		for idx in deselected .indexes ():
			self .update (idx )
	def setSelection (self ,rect ,flags ,_s =[0 ]):
		_s [0 ]+=1
		try :
			firstRow =self .model ().rowCount ()
			lastRow =-1
			row1 =self .indexAt (rect .topLeft ()).row ()
			row2 =self .indexAt (rect .bottomRight ()).row ()
			firstRow =min (row1 ,row2 )
			lastRow =max (row1 ,row2 )
			if firstRow !=self .model ().rowCount ()and lastRow !=-1 :
				selection =QItemSelection (
				self .model ().index (firstRow ,0 ,self .rootIndex ()),
				self .model ().index (lastRow ,0 ,self .rootIndex ())
				)
				self .selectionModel ().select (selection ,flags )
			else :
				invalid =QModelIndex ()
				selection =QItemSelection (invalid ,invalid )
				self .selectionModel ().select (selection ,flags )
		except :
			pass
	def visualRegionForSelection (self ,selection ):
		region =QRegion ()
		for _range in selection :
			for row in range (_range .top (),_range .bottom ()+1 ):
				for column in range (_range .left (),_range .right ()):
					index =self .model ().index (row ,column ,self .rootIndex ())
					region +=self .visualRect (index )
		return region
	def paintEvent (self ,p ):
		painter =QPainter (self .viewport ())
		painter .setRenderHints (QPainter .Antialiasing |QPainter .TextAntialiasing )
		for row in range (self .model ().rowCount (self .rootIndex ())):
			index =self .model ().index (row ,0 ,self .rootIndex ())
			rect =self .viewportRectForRow (row )
			if (not rect .isValid ())or rect .bottom ()<0 or rect .y ()>self .viewport ().height ():
				continue ;
			option =self .viewOptions ()
			option .rect =rect
			if self .selectionModel ().isSelected (index ):
				option .state |=QStyle .State_Selected
			if self .currentIndex ()==index :
				option .state |=QStyle .State_HasFocus
			self .itemDelegate ().paint (painter ,option ,index )
	def paintOutline (self ,painter ,rectangle ):
		rect =rectangle .adjusted (0 ,0 ,-1 ,-1 )
		painter .save ()
		painter .setPen (QPen (self .palette ().dark ().color (),0.5 ));
		painter .drawRect (rect );
		painter .setPen (QPen (Qt .black ,0.5 ));
		painter .drawLine (rect .bottomLeft (),rect .bottomRight ());
		painter .drawLine (rect .bottomRight (),rect .topRight ());
		painter .restore ();
	def resizeEvent (self ,r ):
		self .hashIsDirty =True
		self .calculateRectsIfNecessary ()
		self .updateGeometries ()
	def updateGeometries (self ):
		RowHeight =self .RowHeight +self .ExtraHeight
		self .horizontalScrollBar ().setSingleStep (self .UnitSize )
		self .horizontalScrollBar ().setPageStep (self .viewport ().width ())
		self .horizontalScrollBar ().setRange (0 ,max (0 ,self .idealWidth -self .viewport ().width ()))
		self .verticalScrollBar ().setSingleStep (RowHeight )
		self .verticalScrollBar ().setPageStep (self .viewport ().height ())
		self .verticalScrollBar ().setRange (0 ,max (0 ,self .idealHeight -self .viewport ().height ()))
	def mousePressEvent (self ,event ):
		'''
        '''
		idx =self .indexAt (event .pos ())
		if idx .isValid ():
			self .setCurrentIndex (idx )
		super (QkLineView ,self ).mousePressEvent (event )
	def mouseReleaseEvent (self ,event ):
		super (QkLineView ,self ).mouseReleaseEvent (event )
	def copyToClip (self ):
		'복사'
		try :
			slist =self .selectGroup ()
			clip =self .clipboard
			keul =self .model ().keul [slist [0 ]:slist [-1 ]+1 ]
			zts =keul .toZ3a2s ()
			clip .setText (zts ,QClipboard .Clipboard )
			clip .setText (zts ,QClipboard .Selection )
		except :
			pass
