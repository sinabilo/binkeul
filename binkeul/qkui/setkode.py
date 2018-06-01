from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .listwgt import QkListWgt
from binkeul .qkui .butlab import QkBLabel
from binkeul .betl .bkode import BKodeTb ,BKode
from binkeul .betl .kodekind import KodeKind ,KindVal
from binkeul .base import CONF
from binkeul .binkeul_rc import *
from binkeul import at_end
from functools import partial
def tr (a ):
	return a
class QkSetKindBox (QComboBox ):
	colist =[
	(Qt .black ,Qt .red ),
	(Qt .white ,Qt .darkRed ),
	(Qt .black ,Qt .green ),
	(Qt .white ,Qt .darkGreen ),
	(Qt .white ,Qt .darkBlue ),
	(Qt .black ,Qt .cyan ),
	(Qt .white ,Qt .darkCyan ),
	(Qt .black ,Qt .magenta ),
	(Qt .white ,Qt .darkMagenta ),
	(Qt .black ,Qt .yellow ),
	(Qt .white ,Qt .darkYellow ),
	(Qt .white ,Qt .blue ),
	]
	tytip ={
	1 :"JAKKS",
	8 :"JAKKS",
	13 :"ABBAA",
	24 :"GGGA",
	35 :"KKK",
	44 :"JAKKS",
	53 :"ABBAA",
	64 :"GGGA",
	85 :"KKK",
	}
	def __init__ (self ):
		super ().__init__ ()
		self .initTable ()
		self .setMinimumWidth (60 )
		self .setModel (self .table .model ())
		self .setView (self .table )
		self .activated .connect (self .setKind )
		self .setSizeAdjustPolicy (QComboBox .AdjustToMinimumContentsLength )
		self .setLineEdit (QLineEdit (self ))
		self .lineEdit ().setDragEnabled (False )
		self .setCurrentIndex (-1 )
		self .lineEdit ().mousePressEvent =lambda e :self .lineEdit ().deselect ()or self .view ().isHidden ()or self .showPopup ()
	def initTable (self ):
		self .table =QTableWidget ()
		self .table .setColumnCount (10 )
		self .table .setRowCount (10 )
		self .table .verticalHeader ().hide ()
		self .table .horizontalHeader ().hide ()
		ikind =iter (KodeKind .items ())
		nkind =iter (range (100 ))
		for y in range (10 ):
			self .table .setColumnWidth (y ,40 )
			for x in range (10 ):
				wi =QTableWidgetItem ()
				try :
					_ ,(tykey ,tytip )=next (ikind )
					wi .setText (tykey )
					wi .setToolTip (tytip )
					self .table .setItem (x ,y ,wi )
					co =self .colist [ord (tykey [0 ])%(len (self .colist ))]
					wi .setForeground (co [0 ])
					wi .setBackground (co [1 ])
				except :
					tynum =next (nkind )
					wi .setText (str (tynum ))
					wi .setToolTip (self .tytip .get (tynum ,''))
					self .table .setItem (x ,y ,wi )
					wi .setForeground (Qt .black )
					wi .setBackground (Qt .lightGray )
		self .table .setMinimumWidth (400 )
	def setKind (self ,lev ):
		idx =self .view ().currentIndex ()
		if idx .isValid ():
			kd =self .view ().model ().data (idx )
			if kd :
				self .setEditText (kd )
	@property
	def kind (self ):
		kd =self .lineEdit ().text ()
		if kd in KindVal :
			return KindVal [kd ]
		else :
			return int (kd )
class QkBx4Butgrp (QGroupBox ):
	def __init__ (self ,parent ):
		super ().__init__ (parent =parent )
		self .bx4rbutGrp =QButtonGroup ()
		self .buts =[None ,None ,None ,None ]
		self .bkodes =[None ,None ,None ,None ]
		hlay =QHBoxLayout ()
		for i in range (4 ):
			rbut =QRadioButton ("ABCD"[i ])
			self .buts [i ]=rbut
			self .bx4rbutGrp .addButton (rbut )
			hlay .addWidget (rbut )
		self .setLayout (hlay )
	def setHxs (self ,hxset ,curbkode =None ):
		self .bkodes =list (BKode .getBx4 (hxset ))
		for n ,bkode in enumerate (self .bkodes ):
			if bkode ==curbkode :
				self .buts [n ].setChecked (True )
			elif bkode .inTable ():
				self .buts [n ].setDisabled (True )
			self .buts [n ].clicked .connect (partial (self .parent ().setKode ,bkode ))
class QkSetKodeDlg (QDialog ):
	def __init__ (self ,parent =None ):
		super ().__init__ (parent =parent )
		glay =QGridLayout ()
		self .kodelb =QkBLabel ()
		self .kodelb .setFixedSize (60 ,60 )
		glay .addWidget (self .kodelb ,0 ,0 ,2 ,2 )
		self .kdCmb =QkSetKindBox ()
		glay .addWidget (self .kdCmb ,0 ,2 ,1 ,1 )
		self .bx4rbutGrp =QkBx4Butgrp (self )
		glay .addWidget (self .bx4rbutGrp ,0 ,3 ,1 ,3 )
		self .v_kodeval =QLineEdit ()
		self .v_kodeval .setReadOnly (True )
		self .v_kodeval .setStyleSheet ("""background-color: lightgrey;""")
		self .v_z3a2s =QLineEdit ()
		self .v_z3a2s .setReadOnly (True )
		self .v_z3a2s .setStyleSheet ("""background-color: lightgrey;""")
		glay .addWidget (self .v_kodeval ,1 ,2 ,1 ,2 )
		glay .addWidget (self .v_z3a2s ,1 ,4 ,1 ,2 )
		self .dicTabs =QTabWidget ()
		glay .addWidget (self .dicTabs ,2 ,0 ,3 ,6 )
		self .buttonBox =QDialogButtonBox (Qt .Horizontal )
		self .buttonBox .addButton (QDialogButtonBox .Reset )
		self .buttonBox .addButton (QDialogButtonBox .Cancel )
		self .buttonBox .addButton (QDialogButtonBox .Ok )
		self .buttonBox .rejected .connect (self .reject )
		self .buttonBox .accepted .connect (self .accept )
		self .buttonBox .clicked .connect (self .click )
		glay .addWidget (self .buttonBox ,5 ,0 ,1 ,6 )
		glay .setColumnStretch (0 ,1 )
		glay .setColumnStretch (1 ,1 )
		glay .setColumnStretch (2 ,10 )
		glay .setColumnStretch (3 ,10 )
		glay .setColumnStretch (4 ,10 )
		glay .setColumnStretch (5 ,10 )
		self .setLayout (glay )
	def accept (self ):
		self .saveKode ()
		super ().accept ()
	def reject (self ):
		super ().reject ()
	def click (self ,but ):
		if self .buttonBox .standardButton (but )==QDialogButtonBox .Reset :
			self .setHxs (self .hxset )
		else :
			return
	def setDics (self ,bkode ):
		self .dicTabs .clear ()
		for dic in CONF ["dics-default"]:
			self .dicTabs .addTab (QTextEdit (),dic )
		if bkode .inTable ():
			q =BKodeTb .get (kodeval =bkode .value )
			dics =eval (q .dics )
			tabs ={self .dicTabs .tabText (i ):i
			for i in range (self .dicTabs .count ())}
			for k ,v in dics .items ():
				if k in tabs :
					self .dicTabs .widget (tabs [k ]).setText (v )
				else :
					self .addTab (QTextEdit (v ),k )
	def setHxs (self ,hxset ):
		'''
        '''
		self .hxset =hxset
		if BKodeTb .existHxs (self .hxset ):
			self .bkode =BKodeTb .getBKode (self .hxset )
			self .setWindowTitle ("Update Kode")
			kind =KodeKind .get (
			self .bkode .kind ,
			(str (self .bkode .kind ),'')
			)[0 ]
			self .kdCmb .lineEdit ().setText (kind )
		else :
			self .bkode =BKodeTb .getNew (self .hxset )
			if self .bkode ==None :
				return False
			self .kodelb .setStyleSheet ("QLabel { background-color : gold}")
			self .setWindowTitle ("New Kode")
			self .kdCmb .lineEdit ().setText ('-1')
		self .bx4rbutGrp .setHxs (self .hxset ,curbkode =self .bkode )
		self .setDics (self .bkode )
		self .setKode (self .bkode )
		self .kodelb .setHxs (self .hxset )
	def setKode (self ,bkode ):
		self .v_kodeval .setText (str (bkode .value ))
		self .v_z3a2s .setText (bkode .toZ3a2s ())
		self .bkode =bkode
	def saveKode (self ):
		dics ={}
		for i in range (self .dicTabs .count ()):
			key =self .dicTabs .tabText (i )
			text =self .dicTabs .widget (i ).toPlainText ()
			if text :
				dics [key ]=text
		kind =self .kdCmb .kind
		r =BKodeTb .updateHxs (self .hxset ,bkode =self .bkode ,dics =dics ,kind =kind )
		return r
	@classmethod
	def runModal (cls ,hxset ):
		dialog =cls ()
		if dialog .setHxs (hxset )==False :
			dialog .reject ()
			cannotdlg =QkCannotSetKodeDlg (hxset )
			cannotdlg .exec_ ()
			return 0
		else :
			r =dialog .exec_ ()
			if r :
				return dialog .bkode
			else :
				return 0
class QkCannotSetKodeDlg (QDialog ):
	def __init__ (self ,hxset ,parent =None ):
		super ().__init__ (parent =parent )
		vlay =QVBoxLayout ()
		lwgt =QkListWgt ()
		lwgt .setKodes ([bkode for bkode in BKode .getBx4 (hxset )if bkode .inTable ()])
		vlay .addWidget (lwgt )
		vlay .addWidget (QLabel ('이미 등록된 코드와 충돌합니다. 코드의 일부 획을 변경해야 합니다.'))
		buttonBox =QDialogButtonBox (Qt .Horizontal )
		buttonBox .addButton (QDialogButtonBox .Yes )
		vlay .addWidget (buttonBox )
		self .setLayout (vlay )
