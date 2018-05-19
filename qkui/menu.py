from PySide .QtCore import *
from PySide .QtGui import *
from PySide .QtCore import QTranslator
from binkeul .binkeul_rc import *
from binkeul .betl .keul import Keul
from binkeul .base import CONF
import pdb ,random ,array
class QObj (QObject ):
	def trans (self ,text ):
		return {
		"&Open":self .tr ("&Open"),
		"Exit":self .tr ("Exit"),
		'Exit application':self .tr ('Exit application'),
		"copy":self .tr ("copy"),
		"paste":self .tr ("paste"),
		'&File':self .tr ('&File'),
		'&Edit':self .tr ('&Edit'),
		'edit copy':self .tr ('edit copy'),
		'edit paste':self .tr ('edit paste'),
		'binkeul window menu':self .tr ('binkeul window menu'),
		}[text ]
tr =QObj ().trans
class QkMenuBar (QMenuBar ):
	def __init__ (self ,parent =None ):
		super ().__init__ (parent )
	def setActions (self ):
		if "&Open"in self .act_set :
			openAct =QAction (tr ("&Open"),self )
			openAct .triggered .connect (self .parent ().openFile )
			self .act_set ["&Open"]=openAct
		if "Exit"in self .act_set :
			exitAct =QAction (QIcon (":pics/exit.PNG"),tr ("Exit"),self )
			exitAct .setShortcut ('Ctrl+Q')
			exitAct .setStatusTip (tr ('Exit application'))
			exitAct .triggered .connect (self .parent ().close )
			self .act_set ["Exit"]=exitAct
		if "copy"in self .act_set :
			exitAct =QAction (QIcon (":pics/exit.PNG"),tr ("copy"),self )
			exitAct .setShortcut ('Ctrl+Q')
			exitAct .setStatusTip (tr ('edit copy'))
			exitAct .triggered .connect (self .parent ().close )
			self .act_set ["copy"]=exitAct
		if "paste"in self .act_set :
			exitAct =QAction (QIcon (":pics/exit.PNG"),tr ("paste"),self )
			exitAct .setShortcut ('Ctrl+Q')
			exitAct .setStatusTip (tr ('edit paste'))
			exitAct .triggered .connect (self .parent ().close )
			self .act_set ["paste"]=exitAct
	def initMenu (self ,tree_set ,tool_set =[]):
		self .act_set ={}
		self .tool_set =tool_set
		def walk (m_items ,m_menu =None ):
			for i ,actname in enumerate (m_items ):
				if type (actname )==tuple :
					m =actname
					walk (m [1 ],m [0 ])
				else :
					if actname .startswith ("+"):
						actname =actname [1 :]
						m_items [i ]=actname
						self .tool_set .add (actname )
					self .act_set [actname ]=None
		walk (tree_set )
		self .setActions ()
		self .addMenus (tree_set )
		self .addToolBar ()
	def addMenus (self ,tree_set ):
		def walk (m_items ,m_menu =None ):
			for actname in m_items :
				if type (actname )==tuple :
					m =actname
					m_0 =m_menu .addMenu (tr (m [0 ]))
					walk (m [1 ],m_0 )
				else :
					m_menu .addAction (self .act_set [actname ])
		walk (tree_set ,m_menu =self )
	def addToolBar (self ):
		self .toolbar =QToolBar ("",self .parent ())
		self .parent ().addToolBar (Qt .LeftToolBarArea ,self .toolbar )
		for actname in self .tool_set :
			self .toolbar .addAction (self .act_set [actname ])
class QkMainMenuBar (QkMenuBar ):
	def __init__ (self ,parent ):
		super ().__init__ (parent )
		self .initMenu ([
		('&File',
		["&Open",
		('&Edit',["copy","paste"]),
		"Exit"]
		),
		('&Edit',["copy","paste"])
		],
		tool_set =["Exit"])
