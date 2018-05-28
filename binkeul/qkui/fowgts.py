import random ,pdb ,collections ,enum
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .qkpub import QkKodeSize ,QkToolSize
from binkeul .qkui .butlab import QkIcon
from binkeul .qkui .fodata import *
from binkeul .qkui .fopad import QkFopad
from binkeul .qkui .listwgt import QkListWgt ,QkWListWgt
from binkeul .qkui .setkode import QkSetKodeDlg
from binkeul .betl .bkode import BKodeTb
from binkeul .betl .ukode import UKodeTb
from binkeul .betl .kode import Kode
from binkeul .betl .keul import Keul
from functools import partial
from binkeul .binkeul_rc import *
from binkeul import at_end
class QObj (QObject ):
	def trans (self ,text ):
		return {
		"insert left":self .tr ("insert left"),
		"replace":self .tr ("replace"),
		'insert right':self .tr ('insert right'),
		"undo input":self .tr ("undo input"),
		"redo input":self .tr ("redo input"),
		'clear':self .tr ('clear'),
		'dialog':self .tr ('dialog'),
		}[text ]
tr =QObj ().trans
class QkFoCtrlBut (QPushButton ):
	def __init__ (self ,imgfile ,tooltip =None ):
		pmap =QPixmap (imgfile )
		pmap .setMask (pmap )
		icon =QIcon (pmap )
		super ().__init__ (icon ,'')
		self .setIconSize (QkToolSize )
		if tooltip :
			self .setToolTip (tooltip )
class QkFoCtrlButBox (QVBoxLayout ):
	def __init__ (self ,foboard ,parent =None ):
		super ().__init__ (parent )
		self .foboard =foboard
		set_kode_dlg =QkFoCtrlBut (":/images/fo-dialog.png",tr ("dialog"))
		in_left =QkFoCtrlBut (":/images/fo-insert-left.png",tr ("insert left"))
		in_cur =QkFoCtrlBut (":/images/fo-replace.png",tr ("replace"))
		in_right =QkFoCtrlBut (":/images/fo-insert-right.png",tr ("insert right"))
		but_undo =QkFoCtrlBut (":/images/fo-undo-inupt.png",tr ("undo input"))
		but_redo =QkFoCtrlBut (":/images/fo-redo-input.png",tr ("redo input"))
		but_reset =QkFoCtrlBut (":/images/fo-clear.png",tr ("clear"))
		self .addStretch (0 )
		self .addWidget (set_kode_dlg )
		self .addWidget (in_left )
		self .addWidget (in_cur )
		self .addWidget (in_right )
		self .addWidget (but_undo )
		self .addWidget (but_redo )
		self .addWidget (but_reset )
		self .addStretch (0 )
		set_kode_dlg .clicked .connect (self .act_set_kode_dlg )
		in_left .clicked .connect (partial (self .act_input ,"left"))
		in_cur .clicked .connect (partial (self .act_input ,"cur"))
		in_right .clicked .connect (partial (self .act_input ,"right"))
		but_undo .clicked .connect (self .foboard .fopad .undoDraw )
		but_redo .clicked .connect (self .foboard .fopad .redoDraw )
		but_reset .clicked .connect (self .foboard .fopad .resetDraw )
	def act_set_kode_dlg (self ):
		fod ,_ =self .foboard .fopad .getFoDG ()
		if not fod :return
		bkode =QkSetKodeDlg .runModal (fod .getHxs ())
		if bkode :
			self .foboard .fo_finder .curInsert (bkode )
	def act_input (self ,input_to ):
		kodes =self .foboard .fo_finder .selectedKodes ()
		if not kodes :return
		self .foboard .fo_inputhist .addKeul (kodes )
		if not self .foboard .editor :return
		keul =Keul (kodes )
		if input_to =="left":
			self .foboard .editor .insert (keul )
		elif input_to =="right":
			self .foboard .editor .insertmove (keul )
		elif input_to =="cur":
			self .foboard .editor .replace (keul )
class QkFoFinder (QkListWgt ):
	itemMoved =Signal (int ,int ,QListWidgetItem )
	def __init__ (self ,parent =None ):
		super ().__init__ (
		direction =Qt .LeftToRight ,
		parent =parent )
		self .setHorizontalScrollBarPolicy (Qt .ScrollBarAlwaysOn )
		self .setVerticalScrollBarPolicy (Qt .ScrollBarAlwaysOff )
		self .setMaximumHeight (62 )
		self .setAcceptDrops (True )
		self .setDragDropMode (self .InternalMove )
		self .drag_item =None
		self .drag_row =None
	def dragLeaveEvent (self ,event ):
		r =self .row (self .currentItem ())
		self .kodes .pop (r )
		self .takeItem (r )
	def dropEvent (self ,event ):
		r1 =self .row (self .currentItem ())
		kode =self .kodes .pop (r1 )
		super ().dropEvent (event )
		r2 =self .row (self .currentItem ())
		self .kodes .insert (r2 ,kode )
	def keyPressEvent (self ,e ):
		if e .key ()in (Qt .Key_Delete ,Qt .Key_Backspace ):
			kodes =self .selectedKodes ()
			self .clear ()
			self .setKodes (kodes )
			self .setCurrentRow (0 )
	def curInsert (self ,kode ):
		if kode in self .kodes :
			self .selectionModel ().clear ()
			self .setCurrentRow (self .kodes .index (kode ))
		else :
			row =self .row (self .currentItem ())+1
			self .selectionModel ().clear ()
			item =QListWidgetItem (QkIcon (kode ),"")
			self .insertItem (row ,item )
			self .kodes .insert (row ,kode )
			self .setCurrentRow (row )
	@Slot (Fodata ,Fodata )
	def find (self ,fod ,fog ):
		self .clear ()
		dhxs =fod .getHxs ()
		ghxs =fog .getHxs ()
		limit =50
		kode_list =BKodeTb .findMatch (dhxs ,ghxs ,limit =limit )
		if not kode_list :
			kode_list =BKodeTb .findMatch (dhxs ,dhxs ,limit =limit )
		self .setKodes (kode_list )
		self .setCurrentRow (0 )
	def selectedKodes (self ):
		kodes =[self .kodes [idx .row ()]for idx in self .selectionModel ().selectedIndexes ()]
		return kodes
class QkFoKodeDic (QListWidget ):
	''' '''
	sg_pick_kode =Signal (Kode )
	sg_ppick_kode =Signal (Kode )
	def __init__ (self ,*a ):
		super ().__init__ (*a )
		self .setIconSize (QkToolSize )
		self .clicked .connect (self .pick_kode )
		self .doubleClicked .connect (self .ppick_kode )
		self .kodes =[]
	def kode (self ,idx ):
		return self .kodes [idx .row ()]
	def pick_kode (self ,idx ):
		self .sg_pick_kode .emit (self .kode (idx ))
	def ppick_kode (self ,idx ):
		self .sg_ppick_kode .emit (self .kode (idx ))
	def setKode (self ,bkode ):
		if bkode in self .kodes :
			i =self .kodes .index (bkode )
			self .takeItem (i )
			self .kodes .pop (i )
		item =QListWidgetItem (QkIcon (bkode ),bkode .texts ())
		item .setData (Qt .ToolTipRole ,repr (bkode ))
		self .insertItem (0 ,item )
		self .kodes .insert (0 ,bkode )
		if self .count ()>100 :
			self .takeItem (100 )
			self .kodes .pop (100 )
		self .verticalScrollBar ().setValue (0 )
	def setKodes (self ,kodes ):
		for kode in kodes :
			self .setKode (kode )
class QkFoWordsL (QkWListWgt ):
	def __init__ (self ,foboard ,*a ):
		super ().__init__ (*a )
		self .foboard =foboard
		self .limit =100
		self .setMinimumWidth (300 )
		self .sg_ppick_keul .connect (self .foboard .fo_finder .setKodes )
	def addKeul (self ,keul ):
		if keul in self .keuls :
			self .keuls .remove (keul )
		self .keuls .insert (0 ,keul )
		self .setKeuls (self .keuls [:self .limit ])
class QkFoWords (QkWListWgt ):
	def __init__ (self ,*a ):
		super ().__init__ (*a )
class QkFoKodes (QkListWgt ):
	def __init__ (self ,*a ):
		super ().__init__ (*a )
class QkFoBoard (QWidget ):
	def __init__ (self ):
		super ().__init__ ()
		self .editor =None
		self .fopad =QkFopad ()
		self .fo_controlbox =QkFoCtrlButBox (foboard =self )
		self .fo_finder =QkFoFinder (parent =self )
		self .fo_kodedic =QkFoKodeDic ()
		self .fo_kodes =QkFoKodes ()
		self .fo_words =QkFoWords ()
		lay =QHBoxLayout ()
		lvlay =QVBoxLayout ()
		self .fo_inputhist =QkFoWordsL (self )
		self .fo_searchline =QLineEdit ()
		self .fo_searchbut =QPushButton ("search")
		lvlay .addWidget (self .fo_inputhist )
		lhlay =QHBoxLayout ()
		lhlay .addWidget (self .fo_searchline )
		lhlay .addWidget (self .fo_searchbut )
		lvlay .addLayout (lhlay )
		lay .addLayout (lvlay )
		lay .addLayout (self .fo_controlbox )
		lay .addWidget (self .fopad )
		rvlay =QVBoxLayout ()
		self .tabs =QTabWidget ()
		self .tabs .addTab (self .fo_kodedic ,"dic")
		self .tabs .addTab (self .fo_kodes ,"kodes")
		self .tabs .addTab (self .fo_words ,"words")
		rvlay .addWidget (self .fo_finder )
		rvlay .addWidget (self .tabs )
		lay .addLayout (rvlay ,10 )
		self .setLayout (lay )
		self .resize (1200 ,300 )
		self .setConnects ()
	def setEditor (self ,editor ):
		from binkeul .qkui .lineedit import QkLineEdit
		if editor :
			assert isinstance (editor ,QkLineEdit )
			self .editor =editor
		else :
			self .editor =None
	def setConnects (self ):
		self .fopad .sg_input_step [Fodata ,Fodata ].connect (self .fo_finder .find )
		self .fo_finder .sg_pick_kode [Kode ].connect (self .fo_kodedic .setKode )
		self .fo_finder .sg_ppick_kode [Kode ].connect (self .fopad .resetDraw )
		self .fo_kodedic .sg_ppick_kode [Kode ].connect (self .fo_finder .curInsert )
		self .fo_kodes .sg_ppick_kode [Kode ].connect (self .fo_finder .curInsert )
		self .fo_searchline .returnPressed .connect (self .search_text )
		self .fo_searchbut .clicked .connect (self .search_text )
	def search_text (self ):
		bkodes =BKodeTb .search (self .fo_searchline .text ())
		ukodes =UKodeTb .search (self .fo_searchline .text ())
		kodes =bkodes +ukodes
		self .fo_kodedic .setKodes (kodes )
		self .fo_kodes .setKodes (kodes )
	def keyPressEvent (self ,e ):
		self .fopad .keyPressEvent (e )
	def contextMenuEvent (self ,event ):
		pass
