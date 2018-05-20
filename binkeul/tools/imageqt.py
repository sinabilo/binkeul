from PIL import Image
try :from PySide .QtGui import QImage ,qRgb
except :
	try :from PyQt4 .QtGui import QImage ,qRgb
	except :from PyQt5 .QtGui import QImage ,qRgb
def rgb (r ,g ,b ):
	return qRgb (r ,g ,b )
class ImageQt (QImage ):
	def P모드투명변환 (self ,im ):
		if 'transparency'in im .info :
			i =im .info ['transparency']
			tc =i if type (i )==int else ord (i )
			self .setColor (tc ,0 )
	def __init__ (self ,im ):
		data =None
		colortable =None
		if hasattr (im ,"toUtf8"):
			im =unicode (im .toUtf8 (),"utf-8")
		if Image .isStringType (im ):
			im =Image .open (im )
		if im .mode =="1":
			format =QImage .Format_Mono
		elif im .mode =="L":
			format =QImage .Format_Indexed8
			colortable =[]
			for i in range (256 ):
				colortable .append (rgb (i ,i ,i ))
		elif im .mode =="P":
			format =QImage .Format_Indexed8
			colortable =[]
			palette =im .getpalette ()
			for i in range (0 ,len (palette ),3 ):
				colortable .append (rgb (*palette [i :i +3 ]))
		elif im .mode =="RGB":
			data =im .tobytes ("raw","BGRX")
			format =QImage .Format_RGB32
		elif im .mode in ("RGBA","LA"):
			if im .mode =="LA":im =im .convert ('RGBA')
			try :
				data =im .tobytes ("raw","BGRA")
			except SystemError :
				r ,g ,b ,a =im .split ()
				im =Image .merge ("RGBA",(b ,g ,r ,a ))
			format =QImage .Format_ARGB32
		else :
			raise ValueError ("unsupported image mode %r"%im .mode )
		self .__data =data or im .tobytes ()
		QImage .__init__ (self ,self .__data ,im .size [0 ],im .size [1 ],format )
		if colortable :
			self .setColorTable (colortable )
		if im .mode in ("P","L"):
			self .P모드투명변환 (im )
			pass
