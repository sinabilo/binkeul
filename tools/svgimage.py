from PySide .QtGui import QApplication ,QPixmap
from PySide .QtCore import QIODevice ,QByteArray ,QBuffer ,QCoreApplication
from PySide .QtSvg import QSvgWidget
import sys ,os
if not QCoreApplication .instance ():
	QApplication (sys .argv )
def svgImage (svgfile ,file =None ):
	qs =QSvgWidget ()
	qs .load (svgfile )
	qim =QPixmap .grabWidget (qs )
	bts =QByteArray ()
	buffer =QBuffer (bts )
	buffer .open (QIODevice .WriteOnly )
	qim .save (buffer ,"png")
	bts =buffer .data ().data ()
	buffer .close ()
	if type (file )==str :
		assert os .path .splitext (file )[1 ].lower ()==".png"
		with open (file ,"bw")as f :
			f .write (bts )
	elif hasattr (file ,'write'):
		file .write (bts )
	else :
		return bts
