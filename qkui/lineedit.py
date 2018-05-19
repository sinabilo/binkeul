from PySide .QtGui import QApplication ,QClipboard
from binkeul .qkui .lineview import QkLineView
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .betl .ukode import UKode
from binkeul .betl .bkode import BKode
from binkeul .betl .kode import Kode
from binkeul .betl .keul import Keul
from binkeul .betl .svg import KeulSvgFrm
from binkeul .base import datapath
import pdb
class QkLineEdit (QkLineView ):
	sg_pick_kode =Signal (Kode )
	sg_ppick_kode =Signal (Kode )
	def __init__ (self ,sample =0 ,parent =None ):
		super ().__init__ (sample ,parent )
		self .clicked .connect (self .pick_kode )
		self .doubleClicked .connect (self .ppick_kode )
	def pick_kode (self ):
		index =self .currentIndex ()
		kode =self .model ().keul [index .row ()]
		self .sg_pick_kode .emit (kode )
	def ppick_kode (self ):
		index =self .currentIndex ()
		kode =self .model ().keul [index .row ()]
		self .sg_ppick_kode .emit (kode )
	def rowsInserted (self ,parent ,start ,end ):
		self .hashIsDirty =True
		self .selectionModel ().clearSelection ()
		super (QkLineView ,self ).rowsInserted (parent ,start ,end )
	def rowsAboutToBeRemoved (self ,parent ,start ,end ):
		self .selectionModel ().clearSelection ()
		super (QkLineView ,self ).rowsAboutToBeRemoved (parent ,start ,end )
	def moveCursor (self ,cursorAction ,KeyboardModifiers ):
		index =self .currentIndex ()
		if index .isValid ():
			if (cursorAction ==QAbstractItemView .MoveLeft and index .row ()>0 )or (cursorAction ==QAbstractItemView .MoveRight and index .row ()+1 <self .model ().rowCount ()):
				offset =-1 if cursorAction ==QAbstractItemView .MoveLeft else 1
				index =self .model ().index (index .row ()+offset ,
				index .column (),index .parent ())
			elif (cursorAction ==QAbstractItemView .MoveUp and index .row ()>0 )or (cursorAction ==QAbstractItemView .MoveDown and index .row ()+1 <self .model ().rowCount ()):
				RowHeight =(self .RowHeight +self .ExtraHeight )*(-1 if cursorAction ==QAbstractItemView .MoveUp else 1 )
				rect =self .viewportRectForRow (index .row ())
				point =QPoint (rect .center ().x (),rect .center ().y ()+RowHeight )
				while point .x ()>=0 :
					index =self .indexAt (point );
					if index .isValid ():
						break ;
					point .setX (point .x ()-self .UnitSize )
		return index
	def keyPressEvent (self ,e ):
		if e .key ()==Qt .Key_Backspace :
			self .removeBack ()
			pass
		elif e .key ()==Qt .Key_Delete :
			self .removeSel ()
		elif e .key ()==Qt .Key_Return :
			self .ppick_kode ()
			pass
		elif e .key ()==Qt .Key_Insert :
			pass
		elif e .key ()in (
		Qt .Key_Left ,
		Qt .Key_Up ,
		Qt .Key_Right ,
		Qt .Key_Down ,):
			super (QkLineView ,self ).keyPressEvent (e )
	def insert (self ,keul ,right =False ):
		cur =self .currentIndex ().row ()
		if cur <0 :cur =0
		elif right :cur +=1
		self .model ().insertRows (cur ,keul )
		self .updateall ()
		self .setCurrentIndex (self .currentIndex ())
	def replace (self ,keul ):
		cur =self .currentIndex ().row ()
		self .model ().removeRows (cur ,cur )
		self .model ().insertRows (cur ,keul )
		self .updateall ()
		idx =self .model ().index (cur +len (keul )-1 )
		self .setCurrentIndex (idx )
	def removeBack (self ):
		r =self .currentIndex ().row ()-1
		if r <0 :return
		self .model ().removeRows (r ,r )
		self .updateall ()
		self .setCurrentIndex (self .currentIndex ())
	def removeSel (self ):
		slist =self .selectGroup ()
		p_idx =self .currentIndex ()
		a =self .model ().removeRows (slist [0 ],slist [-1 ])
		self .updateall ()
		idx =self .currentIndex ()
		if not (p_idx .row ()==idx .row ()==0 ):
			idx =self .model ().index (idx .row ()+1 )
		if idx .isValid ():
			self .setCurrentIndex (idx )
	def cutToClip (self ):
		try :
			slist =self .selectGroup ()
			p_idx =self .currentIndex ()
			keul =self .model ().keul [slist [0 ]:slist [-1 ]+1 ]
			zts =keul .toZ3a2s ()
			clip =self .clipboard
			clip .setText (zts ,QClipboard .Clipboard )
			clip .setText (zts ,QClipboard .Selection )
			a =self .model ().removeRows (slist [0 ],slist [-1 ])
			self .updateall ()
			idx =self .currentIndex ()
			if not (p_idx .row ()==idx .row ()==0 ):
				idx =self .model ().index (idx .row ()+1 )
			if idx .isValid ():
				self .setCurrentIndex (idx )
		except :
			pass
	def clearSel (self ):
		'선택해제'
		self .selectionModel ().clearSelection ()
	def pasteFromClip (self ):
		'붙여넣기'
		try :
			clip =self .clipboard
			zts =clip .text ()
			keul =Keul .fromZ3a2s (zts )
			self .insert (keul )
		except :
			pass
	@Slot ()
	def writeSvg (self ):
		'svg 저장'
		class Worker (QThread ):
			def __init__ (self ,model ,ret ):
				super ().__init__ ()
				self .model =model
				self .ret =ret
				svgconf ={
				"stroke-width":0 ,
				"stroke":'gray',
				"fill":'#515A5B',
				}
				self .svgeng =KeulSvgFrm (scale =2 ,svgconf =svgconf )
				self .svgeng .layout .limit =500
				self .svgeng .layout .usedefs =True
				self .upath =None
			def run (self ):
				import webbrowser ,os ,tempfile ,pathlib
				model =self .model
				tf =tempfile .NamedTemporaryFile (dir =datapath ('temp'),delete =False ,suffix ='.svg')
				tf .close ()
				self .ret ["upath"]=pathlib .Path (tf .name ).as_uri ()
				self .svgeng .make (model .keul ,file =tf .name )
				webbrowser .open_new (ret ["upath"])
			def __del__ (self ):
				self .wait ()
		ret ={}
		w =Worker (self .model ,ret )
		w .start ()
