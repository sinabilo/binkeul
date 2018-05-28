from PySide import QtCore ,QtGui
import sys
from PySide .QtGui import QIcon ,QMainWindow ,QTextEdit ,QAction ,QApplication ,QTabWidget ,QDockWidget ,QToolBar
from PySide .QtCore import QTranslator ,Signal ,QEvent
from PySide .QtCore import Qt ,QCoreApplication
from binkeul .base import CONF ,datapath
from binkeul .binkeul_rc import *
from binkeul .betl .keul import Keul
from binkeul .betl .kode import Kode
from binkeul .qkui .fowgts import QkFoBoard
from binkeul .qkui .savesvg import QkSaveSvgDlg
from binkeul .qkui .lineview import QkLineView ,QkLineDoc ,QkLineDelegate
from binkeul .qkui .lineedit import QkLineEdit
from binkeul import at_end
from binkeul .binkeul_rc import *
import copy
translator =QTranslator ()
class MdiChild (QkLineEdit ):
	sequenceNumber =1
	def __init__ (self ):
		super (MdiChild ,self ).__init__ ()
		self .setAttribute (QtCore .Qt .WA_DeleteOnClose )
		self .isUntitled =True
	def newFile (self ):
		self .isUntitled =True
		self .curFile ="document%d.keul"%MdiChild .sequenceNumber
		MdiChild .sequenceNumber +=1
		self .setWindowTitle (self .curFile +'[*]')
		model =QkLineDoc (Keul (),self )
		self .setModel (model )
		self .model ().contentsChanged .connect (self .documentWasModified )
	def loadFile (self ,fileName ):
		file =QtCore .QFile (fileName )
		if not file .open (QtCore .QFile .ReadWrite ):
			QtGui .QMessageBox .warning (self ,"MDI",
			"Cannot read file %s:\n%s."%(fileName ,file .errorString ()))
			return False
		keul =Keul .fromBytes (file .readAll ().data ())
		QtGui .QApplication .setOverrideCursor (QtCore .Qt .WaitCursor )
		self .setModel (QkLineDoc (keul ,self ))
		QtGui .QApplication .restoreOverrideCursor ()
		self .setCurrentFile (fileName )
		self .model ().contentsChanged .connect (self .documentWasModified )
		return True
	def save (self ):
		if self .isUntitled :
			return self .saveAs ()
		else :
			return self .saveFile (self .curFile )
	def saveAs (self ):
		fileName ,filtr =QtGui .QFileDialog .getSaveFileName (self ,"Save As",
		self .curFile )
		if not fileName :
			return False
		return self .saveFile (fileName )
	def saveFile (self ,fileName ):
		file =QtCore .QFile (fileName )
		if not file .open (QtCore .QFile .WriteOnly ):
			QtGui .QMessageBox .warning (self ,"MDI",
			"Cannot write file %s:\n%s."%(fileName ,file .errorString ()))
			return False
		QtGui .QApplication .setOverrideCursor (QtCore .Qt .WaitCursor )
		bts =self .model ().keul .toBytes ()
		file .write (QtCore .QByteArray (bts ))
		QtGui .QApplication .restoreOverrideCursor ()
		self .setCurrentFile (fileName )
		return True
	def saveSvg (self ):
		return QkSaveSvgDlg .runModal (self .model ().keul ,self .curFile )
	def userFriendlyCurrentFile (self ):
		return self .strippedName (self .curFile )
	def currentFile (self ):
		return self .curFile
	def closeEvent (self ,event ):
		if self .maybeSave ():
			event .accept ()
		else :
			event .ignore ()
	def documentWasModified (self ):
		self .setWindowModified (self .model ().isModified ())
	def maybeSave (self ):
		if self .model ().isModified ():
			ret =QtGui .QMessageBox .warning (self ,"MDI",
			"'%s' has been modified.\nDo you want to save your "
			"changes?"%self .userFriendlyCurrentFile (),
			QtGui .QMessageBox .Save |QtGui .QMessageBox .Discard |
			QtGui .QMessageBox .Cancel )
			if ret ==QtGui .QMessageBox .Save :
				return self .save ()
			elif ret ==QtGui .QMessageBox .Cancel :
				return False
		return True
	def setCurrentFile (self ,fileName ):
		self .curFile =QtCore .QFileInfo (fileName ).canonicalFilePath ()
		self .isUntitled =False
		self .model ().setModified (False )
		self .setWindowModified (False )
		self .setWindowTitle (self .userFriendlyCurrentFile ()+"[*]")
	def strippedName (self ,fullFileName ):
		return QtCore .QFileInfo (fullFileName ).fileName ()
class MainWindow (QtGui .QMainWindow ):
	def __init__ (self ):
		super (MainWindow ,self ).__init__ ()
		self .mdiArea =QtGui .QMdiArea ()
		self .mdiArea .setHorizontalScrollBarPolicy (QtCore .Qt .ScrollBarAsNeeded )
		self .mdiArea .setVerticalScrollBarPolicy (QtCore .Qt .ScrollBarAsNeeded )
		self .setCentralWidget (self .mdiArea )
		self .mdiArea .subWindowActivated .connect (self .updateMenus )
		self .mdiArea .subWindowActivated .connect (self .setFoboard )
		self .windowMapper =QtCore .QSignalMapper (self )
		self .windowMapper .mapped .connect (self .setActiveSubWindow )
		self .createActions ()
		self .createMenus ()
		self .createToolBars ()
		self .createStatusBar ()
		self .updateMenus ()
		self .readSettings ()
		self .setWindowTitle ("빈글코드 편집기")
		self .setUnifiedTitleAndToolBarOnMac (True )
		self .foboard =QkFoBoard ()
		self .initDock ()
	def initDock (self ):
		dock =QDockWidget ("foboard",self )
		dock .setAllowedAreas (Qt .TopDockWidgetArea |Qt .BottomDockWidgetArea )
		dock .setWidget (self .foboard )
		self .addDockWidget (Qt .BottomDockWidgetArea ,dock )
	def closeEvent (self ,event ):
		self .mdiArea .closeAllSubWindows ()
		if self .activeMdiChild ():
			event .ignore ()
		else :
			self .writeSettings ()
			event .accept ()
	def newFile (self ):
		child =self .createMdiChild ()
		child .newFile ()
		child .show ()
		child .sel_current_change .connect (self .statusBar ().showMessage )
	def open (self ):
		fileName ,filtr =QtGui .QFileDialog .getOpenFileName (self )
		if fileName :
			existing =self .findMdiChild (fileName )
			if existing :
				self .mdiArea .setActiveSubWindow (existing )
				child =existing .widget ()
				child .sel_current_change .connect (self .statusBar ().showMessage )
				return
			child =self .createMdiChild ()
			if child .loadFile (fileName ):
				self .statusBar ().showMessage ("File loaded",2000 )
				child .show ()
			else :
				child .close ()
	def save (self ):
		if self .activeMdiChild ()and self .activeMdiChild ().save ():
			self .statusBar ().showMessage ("File saved",2000 )
	def saveAs (self ):
		if self .activeMdiChild ()and self .activeMdiChild ().saveAs ():
			self .statusBar ().showMessage ("File saved",2000 )
	def saveSvg (self ):
		if self .activeMdiChild ()and self .activeMdiChild ().saveSvg ():
			self .statusBar ().showMessage ("Svg saved",2000 )
	def delete (self ):
		if self .activeMdiChild ():
			self .activeMdiChild ().removeSel ()
	def deleteBack (self ):
		if self .activeMdiChild ():
			self .activeMdiChild ().removeBack ()
	def cut (self ):
		if self .activeMdiChild ():
			self .activeMdiChild ().cutToClip ()
	def copy (self ):
		if self .activeMdiChild ():
			self .activeMdiChild ().copyToClip ()
	def paste (self ):
		if self .activeMdiChild ():
			self .activeMdiChild ().pasteFromClip ()
	def about (self ):
		QtGui .QMessageBox .about (self ,
		"""빈글코드에디터에 대하여""",
		""" 프로그램 설치를 환영합니다! <br><br> 설치에 대한 도움과 사용자를 위한 설명서는 다음의 링크들을 참고하기 바랍니다. <br> ☞ <a href="https://github.com/sinabilo/binkeul">소스저장소</a> <br> ☞ <a href="https://sites.google.com/site/binkeul/binkeuleditor">빈글코드에디터</a><br><br>"""
		"""
또한 제작자에 문의를 하려면 <a href="mailto:siblo@naver.com">siblo@naver.com</a> 로 메일을 보내세요. 메일을 자주 확인하지는 않습니다. 감사합니다.
""")
	def setFoboard (self ):
		if self .activeMdiChild ():
			self .foboard .setEditor (self .activeMdiChild ())
			try :
				self .activeMdiChild ().sg_ppick_kode [Kode ].disconnect (self .foboard .fo_finder .curInsert )
			except :
				pass
			self .activeMdiChild ().sg_ppick_kode [Kode ].connect (self .foboard .fo_finder .curInsert )
	def updateMenus (self ):
		hasMdiChild =(self .activeMdiChild ()is not None )
		self .saveAct .setEnabled (hasMdiChild )
		self .saveAsAct .setEnabled (hasMdiChild )
		self .saveSvgAct .setEnabled (hasMdiChild )
		self .pasteAct .setEnabled (hasMdiChild )
		self .closeAct .setEnabled (hasMdiChild )
		self .closeAllAct .setEnabled (hasMdiChild )
		self .tileAct .setEnabled (hasMdiChild )
		self .cascadeAct .setEnabled (hasMdiChild )
		self .nextAct .setEnabled (hasMdiChild )
		self .previousAct .setEnabled (hasMdiChild )
		self .separatorAct .setVisible (hasMdiChild )
		hasSelection =(self .activeMdiChild ()is not None and
		self .activeMdiChild ().selectionModel ().hasSelection ())
		self .cutAct .setEnabled (hasSelection )
		self .copyAct .setEnabled (hasSelection )
	def updateWindowMenu (self ):
		self .windowMenu .clear ()
		self .windowMenu .addAction (self .closeAct )
		self .windowMenu .addAction (self .closeAllAct )
		self .windowMenu .addSeparator ()
		self .windowMenu .addAction (self .tileAct )
		self .windowMenu .addAction (self .cascadeAct )
		self .windowMenu .addSeparator ()
		self .windowMenu .addAction (self .nextAct )
		self .windowMenu .addAction (self .previousAct )
		self .windowMenu .addAction (self .separatorAct )
		windows =self .mdiArea .subWindowList ()
		self .separatorAct .setVisible (len (windows )!=0 )
		for i ,window in enumerate (windows ):
			child =window .widget ()
			text ="%d %s"%(i +1 ,child .userFriendlyCurrentFile ())
			if i <9 :
				text ='&'+text
			action =self .windowMenu .addAction (text )
			action .setCheckable (True )
			action .setChecked (child ==self .activeMdiChild ())
			action .triggered .connect (self .windowMapper .map )
			self .windowMapper .setMapping (action ,i )
	def createMdiChild (self ):
		child =MdiChild ()
		self .mdiArea .addSubWindow (child )
		child .copyAvailable .connect (self .cutAct .setEnabled )
		child .copyAvailable .connect (self .copyAct .setEnabled )
		return child
	def createActions (self ):
		self .newAct =QtGui .QAction (QtGui .QIcon (':/images/new.png'),"&New",
		self ,shortcut =QtGui .QKeySequence .New ,
		statusTip ="Create a new file",triggered =self .newFile )
		self .openAct =QtGui .QAction (QtGui .QIcon (':/images/open.png'),
		"&Open...",self ,shortcut =QtGui .QKeySequence .Open ,
		statusTip ="Open an existing file",triggered =self .open )
		self .saveAct =QtGui .QAction (QtGui .QIcon (':/images/save.png'),
		"&Save",self ,shortcut =QtGui .QKeySequence .Save ,
		statusTip ="Save the document to disk",triggered =self .save )
		self .saveAsAct =QtGui .QAction ("Save &As...",self ,
		shortcut =QtGui .QKeySequence .SaveAs ,
		statusTip ="Save the document under a new name",
		triggered =self .saveAs )
		self .saveSvgAct =QtGui .QAction ("Save Svg...",self ,
		statusTip ="Save the document as Svg",
		triggered =self .saveSvg )
		self .exitAct =QtGui .QAction ("E&xit",self ,shortcut ="Ctrl+Q",
		statusTip ="Exit the application",
		triggered =QtGui .qApp .closeAllWindows )
		self .cutAct =QtGui .QAction (QtGui .QIcon (':/images/cut.png'),"Cu&t",
		self ,shortcut =QtGui .QKeySequence .Cut ,
		statusTip ="Cut the current selection's contents to the clipboard",
		triggered =self .cut )
		self .copyAct =QtGui .QAction (QtGui .QIcon (':/images/copy.png'),
		"&Copy",self ,shortcut =QtGui .QKeySequence .Copy ,
		statusTip ="Copy the current selection's contents to the clipboard",
		triggered =self .copy )
		self .pasteAct =QtGui .QAction (QtGui .QIcon (':/images/paste.png'),
		"&Paste",self ,shortcut =QtGui .QKeySequence .Paste ,
		statusTip ="Paste the clipboard's contents into the current selection",
		triggered =self .paste )
		self .closeAct =QtGui .QAction ("Cl&ose",self ,shortcut ="Ctrl+F4",
		statusTip ="Close the active window",
		triggered =self .mdiArea .closeActiveSubWindow )
		self .closeAllAct =QtGui .QAction ("Close &All",self ,
		statusTip ="Close all the windows",
		triggered =self .mdiArea .closeAllSubWindows )
		self .tileAct =QtGui .QAction ("&Tile",self ,
		statusTip ="Tile the windows",
		triggered =self .mdiArea .tileSubWindows )
		self .cascadeAct =QtGui .QAction ("&Cascade",self ,
		statusTip ="Cascade the windows",
		triggered =self .mdiArea .cascadeSubWindows )
		self .nextAct =QtGui .QAction ("Ne&xt",self ,
		shortcut =QtGui .QKeySequence .NextChild ,
		statusTip ="Move the focus to the next window",
		triggered =self .mdiArea .activateNextSubWindow )
		self .previousAct =QtGui .QAction ("Pre&vious",self ,
		shortcut =QtGui .QKeySequence .PreviousChild ,
		statusTip ="Move the focus to the previous window",
		triggered =self .mdiArea .activatePreviousSubWindow )
		self .separatorAct =QtGui .QAction (self )
		self .separatorAct .setSeparator (True )
		self .aboutAct =QtGui .QAction ("&About",self ,
		statusTip ="Show the application's About box",
		triggered =self .about )
		self .aboutQtAct =QtGui .QAction ("About &Qt",self ,
		statusTip ="Show the Qt library's About box",
		triggered =QtGui .qApp .aboutQt )
	def createMenus (self ):
		self .fileMenu =self .menuBar ().addMenu ("&File")
		self .fileMenu .addAction (self .newAct )
		self .fileMenu .addAction (self .openAct )
		self .fileMenu .addAction (self .saveAct )
		self .fileMenu .addAction (self .saveAsAct )
		self .fileMenu .addAction (self .saveSvgAct )
		self .fileMenu .addSeparator ()
		action =self .fileMenu .addAction ("Switch layout direction")
		action .triggered .connect (self .switchLayoutDirection )
		self .fileMenu .addAction (self .exitAct )
		self .editMenu =self .menuBar ().addMenu ("&Edit")
		self .editMenu .addAction (self .cutAct )
		self .editMenu .addAction (self .copyAct )
		self .editMenu .addAction (self .pasteAct )
		self .windowMenu =self .menuBar ().addMenu ("&Window")
		self .updateWindowMenu ()
		self .windowMenu .aboutToShow .connect (self .updateWindowMenu )
		self .menuBar ().addSeparator ()
		self .helpMenu =self .menuBar ().addMenu ("&Help")
		self .helpMenu .addAction (self .aboutAct )
		self .helpMenu .addAction (self .aboutQtAct )
	def createToolBars (self ):
		self .fileToolBar =QToolBar ("File",self )
		self .fileToolBar .addAction (self .newAct )
		self .fileToolBar .addAction (self .openAct )
		self .fileToolBar .addAction (self .saveAct )
		self .addToolBar (Qt .LeftToolBarArea ,self .fileToolBar )
		self .editToolBar =QToolBar ("Edit",self )
		self .editToolBar .addAction (self .cutAct )
		self .editToolBar .addAction (self .copyAct )
		self .editToolBar .addAction (self .pasteAct )
		self .addToolBar (Qt .LeftToolBarArea ,self .editToolBar )
	def createStatusBar (self ):
		self .statusBar ().showMessage ("Ready")
	def readSettings (self ):
		settings =QtCore .QSettings ('Trolltech','MDI Example')
		pos =settings .value ('pos',QtCore .QPoint (200 ,200 ))
		size =settings .value ('size',QtCore .QSize (400 ,400 ))
		self .move (pos )
		self .resize (size )
	def writeSettings (self ):
		settings =QtCore .QSettings ('Trolltech','MDI Example')
		settings .setValue ('pos',self .pos ())
		settings .setValue ('size',self .size ())
	def activeMdiChild (self ):
		activeSubWindow =self .mdiArea .activeSubWindow ()
		if activeSubWindow :
			return activeSubWindow .widget ()
		return None
	def findMdiChild (self ,fileName ):
		canonicalFilePath =QtCore .QFileInfo (fileName ).canonicalFilePath ()
		for window in self .mdiArea .subWindowList ():
			if window .widget ().currentFile ()==canonicalFilePath :
				return window
		return None
	def switchLayoutDirection (self ):
		if self .layoutDirection ()==QtCore .Qt .LeftToRight :
			QtGui .qApp .setLayoutDirection (QtCore .Qt .RightToLeft )
		else :
			QtGui .qApp .setLayoutDirection (QtCore .Qt .LeftToRight )
	def setActiveSubWindow (self ,i ):
		windows =self .mdiArea .subWindowList ()
		if windows [i ]:
			self .mdiArea .setActiveSubWindow (windows [i ])
	def eventFilter (self ,obj ,e ):
		if e .type ()==QEvent .KeyPress :
			if obj in (self .foboard .fo_searchline ,):
				return super ().eventFilter (obj ,e )
			if e .key ()in (Qt .Key_Left ,Qt .Key_Right ,Qt .Key_Backspace ):
				editor =self .activeMdiChild ()
				if editor and (obj is not editor ):
					editor .keyPressEvent (e )
					return True
			elif e .key ()==Qt .Key_Return :
				editor =self .activeMdiChild ()
				if editor :
					editor .ppick_kode ()
				return True
			elif e .key ()in (
			Qt .Key_1 ,
			Qt .Key_2 ,
			Qt .Key_3 ,):
				if e .key ()==Qt .Key_1 :
					self .foboard .fo_controlbox .act_input ("left")
				elif e .key ()==Qt .Key_2 :
					self .foboard .fo_controlbox .act_input ("cur")
				elif e .key ()==Qt .Key_3 :
					self .foboard .fo_controlbox .act_input ("right")
				return True
			elif e .key ()==Qt .Key_F10 :
				self .resize (1000 ,600 )
		return super ().eventFilter (obj ,e )
if __name__ =='''__main__''':
	import sys ,pdb
	from binkeul import main_start
	app =QCoreApplication .instance ()or QApplication (sys .argv )
	QApplication .setWindowIcon (QIcon (':/images/betlapp.PNG'))
	translator .load (datapath ("data","i18n","ko_KO.qm"))
	app .installTranslator (translator )
	mainWin =MainWindow ()
	app .installEventFilter (mainWin )
	mainWin .show ()
	sys .exit (app .exec_ ())
