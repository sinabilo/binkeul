from PySide .QtCore import *
from PySide .QtGui import *
from PySide import QtCore ,QtGui
from binkeul .betl .pubcls import Sz ,FixStyle ,SizeStyle
from binkeul .betl .svg import KeulSvgFrm
from binkeul .binkeul_rc import *
from binkeul import at_end
from collections import namedtuple
from pathlib import Path
import os ,tempfile
import webbrowser
class QkNumComboBox (QComboBox ):
	def __init__ (self ,rg =range (0 ),default =None ,parent =None ):
		super ().__init__ (parent )
		self .addItems ([str (n )for n in rg ])
		if default :
			for i in range (self .count ()):
				if int (self .itemText (i ))>=default :
					self .setCurrentIndex (i )
					break
	def value (self ):
		return int (self .currentText ())
SvgSetting =namedtuple ("SvgSetting",[
"scale","pic2x","limit","margin","space"])
class QkSaveSvgDlg (QDialog ):
	def __init__ (self ,keul ,docfilename ,parent =None ):
		super ().__init__ (parent =parent )
		self .results ={}
		self .tmpfile =tempfile .NamedTemporaryFile (delete =False ,suffix =".svg",dir =os .getcwd ())
		self .tmpfile .close ()
		self .keul =keul
		self .setWindowTitle ("[{}] save to SVG".format (docfilename ))
		self .fileName =os .path .splitext (docfilename )[0 ]+".svg"
		glay =QGridLayout ()
		self .filebut =QPushButton ("파일")
		self .filelab =QLineEdit (self .fileName )
		glay .addWidget (self .filelab ,0 ,0 ,1 ,5 )
		glay .addWidget (self .filebut ,0 ,5 ,1 ,1 )
		glay .setRowMinimumHeight (0 ,50 )
		self .ScaleCmb =QkNumComboBox (range (2 ,5 ))
		self .Pic2xCkb =QCheckBox ()
		self .LimitCmb =QkNumComboBox (range (100 ,1000 ,50 ),300 )
		self .HMgCmb =QkNumComboBox (range (1 ,7 ))
		self .VMgCmb =QkNumComboBox (range (1 ,7 ))
		self .HSpCmb =QkNumComboBox (range (1 ,7 ))
		self .VSpCmb =QkNumComboBox (range (1 ,7 ))
		glay .addWidget (QLabel ("scale"),1 ,0 ,1 ,1 )
		glay .addWidget (QLabel ("pic 2x"),2 ,0 ,1 ,1 )
		glay .addWidget (QLabel ("limit"),3 ,0 ,1 ,1 )
		glay .addWidget (self .ScaleCmb ,1 ,1 ,1 ,1 )
		glay .addWidget (self .Pic2xCkb ,2 ,1 ,1 ,1 )
		glay .addWidget (self .LimitCmb ,3 ,1 ,1 ,1 )
		glay .addWidget (QLabel ("H Margin"),5 ,0 ,1 ,1 )
		glay .addWidget (QLabel ("V Margin"),5 ,3 ,1 ,1 )
		glay .addWidget (self .HMgCmb ,5 ,1 ,1 ,1 )
		glay .addWidget (self .VMgCmb ,5 ,4 ,1 ,1 )
		glay .addWidget (QLabel ("H Space"),6 ,0 ,1 ,1 )
		glay .addWidget (QLabel ("V Space"),6 ,3 ,1 ,1 )
		glay .addWidget (self .HSpCmb ,6 ,1 ,1 ,1 )
		glay .addWidget (self .VSpCmb ,6 ,4 ,1 ,1 )
		line =QFrame ()
		line .setFrameShape (QFrame .HLine )
		line .setFrameShadow (QFrame .Sunken )
		glay .addWidget (line ,9 ,0 ,1 ,6 )
		glay .setRowMinimumHeight (9 ,50 )
		self .prevbut =QPushButton ("Preview")
		glay .addWidget (self .prevbut ,10 ,0 ,1 ,1 )
		self .viewcodebut =QPushButton ("View Code")
		glay .addWidget (self .viewcodebut ,10 ,1 ,1 ,1 )
		self .buttonBox =QDialogButtonBox (Qt .Horizontal )
		self .buttonBox .addButton (QDialogButtonBox .Cancel )
		self .buttonBox .addButton (QDialogButtonBox .Ok )
		glay .addWidget (self .buttonBox ,10 ,2 ,1 ,4 )
		for n in range (6 ):
			glay .setColumnStretch (n ,50 )
			glay .setColumnMinimumWidth (n ,80 )
		self .setLayout (glay )
		self .prevbut .clicked .connect (self .previewSvg )
		self .viewcodebut .clicked .connect (self .viewSvgCode )
		self .filebut .clicked .connect (self .setFileName )
		self .buttonBox .rejected .connect (self .reject )
		self .buttonBox .accepted .connect (self .accept )
	def getKey (self ):
		return SvgSetting (
		scale =self .ScaleCmb .value (),
		pic2x =SizeStyle .pic2x if self .Pic2xCkb .isChecked ()else SizeStyle .pic1x ,
		limit =self .LimitCmb .value (),
		margin =Sz (self .HMgCmb .value (),self .VMgCmb .value ()),
		space =Sz (self .HSpCmb .value (),self .VSpCmb .value ())
		)
	def makeSvg (self ,save =False ):
		key =self .getKey ()
		if key in self .results :
			svg =self .results [key ]
		else :
			mk =KeulSvgFrm (scale =key .scale )
			mk .layout .margin =key .margin
			mk .layout .space =key .space
			mk .layout .limit =key .limit
			mk .layout .usedefs =True
			mk .layout .b64img =True
			mk .layout .conf ["ukode-size-style"]=key .pic2x
			svg =mk .make (self .keul )
			self .results [key ]=svg
		if save :
			with open (self .fileName ,"wb")as f :
				f .write (svg )
		else :
			return svg
	def previewSvg (self ):
		svg =self .makeSvg ()
		with open (self .tmpfile .name ,"wb")as tf :
			tf .write (svg )
		tf_url =Path (self .tmpfile .name ).as_uri ()
		webbrowser .open_new_tab (tf_url )
	def viewSvgCode (self ):
		svg =self .makeSvg ()
		svgcode =str (svg ,"utf8")
		mb =QtGui .QMessageBox (self )
		mb .setDetailedText (svgcode )
		mb .setWindowTitle ("svg code")
		mb .setText (svgcode [:1000 ])
		mb .exec_ ()
	def setFileName (self ):
		fileName ,filtr =QtGui .QFileDialog .getSaveFileName (self ,filter ="*.svg")
		if fileName :
			self .fileName =fileName
			self .filelab .setText (self .fileName )
	@classmethod
	def runModal (cls ,keul =None ,docfilename =''):
		dialog =cls (keul ,docfilename )
		r =dialog .exec_ ()
		return r
	def done (self ,r ):
		os .remove (self .tmpfile .name )
		return super ().done (r )
	def accept (self ):
		self .makeSvg (True )
		super ().accept ()
	def reject (self ):
		super ().reject ()
