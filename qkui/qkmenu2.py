from PySide .QtCore import *
from PySide .QtGui import *
from PySide .QtCore import QTranslator
from binkeul .binkeul_rc import *
from binkeul .betl .ukode import UKode
from binkeul .betl .bkode import BKode
from binkeul .betl .keul import Keul
from binkeul .betl .pubcls import FixStyle
from binkeul import at_end
from binkeul .base import CONF
from binkeul .qkui .kodemap import KodeMapFrm
import pdb ,random ,array
class QkMenuBar (QMenuBar ):
	def __init__ (self ,parent ):
		super ().__init__ (parent )
		self .act ={}
		self .names ={
		"exit":self .tr ("Exit")
		}
		self .setActions ()
		self .addMenus ()
		self .addToolBar ()
	def setActions (self ):
		exitAct =QAction (QIcon (":pics/exit.PNG"),self .names ["exit"],self )
		exitAct .setShortcut ('Ctrl+Q')
		exitAct .setStatusTip (self .tr ('Exit application'))
		exitAct .triggered .connect (self .parent ().close )
		self .act ["exit"]=exitAct
	def addMenus (self ):
		self .fileMenu =self .addMenu (self .tr ('&File'))
		self .fileMenu .addAction (self .tr ("&Open"),self .parent ().openFile ,"Ctrl+O")
		self .fileMenu .addAction (QIcon (":pics/exit.PNG"),self .tr ("Exit"),self .parent ().close ,"Ctrl+Q")
		self .fileMenu .addAction (self .act ["exit"])
	def addToolBar (self ):
		self .toolbar =QToolBar ("",self .parent ())
		self .parent ().addToolBar (Qt .LeftToolBarArea ,self .toolbar )
		self .toolbar .addAction (self .act ["exit"])
