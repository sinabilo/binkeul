import sys
from PySide .QtGui import QIcon ,QMainWindow ,QTextEdit ,QAction ,QApplication ,QTabWidget ,QDockWidget
from PySide .QtCore import QTranslator
from PySide .QtCore import Qt ,QCoreApplication
from binkeul .base import CONF ,datapath
from binkeul .binkeul_rc import *
from binkeul .qkui .fowgts import QkFoBoard
from binkeul .qkui .lineview import QkLineView ,QkLineDelegate
from binkeul import at_end
translator =QTranslator ()
class QkMainWin (QMainWindow ):
	def __init__ (self ):
		super ().__init__ ()
		self .initDock ()
		self .initUI ()
	def initDock (self ):
		dock =QDockWidget ("binctrl",self )
		dock .setAllowedAreas (Qt .TopDockWidgetArea |Qt .BottomDockWidgetArea )
		dock .setWidget (QkFoBoard ())
		self .addDockWidget (Qt .BottomDockWidgetArea ,dock )
	def initUI (self ):
		textEdit1 =QkLineView (sample =10 )
		textEdit2 =QkLineView (sample =100 )
		textEdit3 =QkLineView (sample =200 )
		tabs =QTabWidget ()
		tabs .addTab (textEdit1 ,"TAB1")
		tabs .addTab (textEdit2 ,"TAB2")
		tabs .addTab (textEdit3 ,"TAB3")
		tabs .setMovable (True )
		self .setCentralWidget (tabs )
		exitAct =QAction (QIcon (":pics/exit.PNG"),self .tr ("Exit"),self )
		exitAct .setShortcut ('Ctrl+Q')
		exitAct .setStatusTip (self .tr ('Exit application'))
		exitAct .triggered .connect (self .close )
		self .statusBar ()
		menubar =self .menuBar ()
		fileMenu =menubar .addMenu (self .tr ('&File'))
		fileMenu .addAction (exitAct )
		toolbar =self .addToolBar (self .tr ('Exit'))
		toolbar .addAction (exitAct )
		toolbar .addAction (exitAct )
		self .setGeometry (300 ,300 ,350 ,250 )
		self .setWindowTitle (self .tr ('binkeul main window'))
		self .show ()
	def setmenu (self ):
		pass
