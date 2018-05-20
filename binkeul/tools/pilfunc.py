from PIL import Image ,ImageDraw ,ImageOps ,ImageFilter
from binkeul .tools import imageqt
import tempfile ,base64
def set_alpha (im ):
	assert im .mode =="RGBA"
	co =im .getpixel ((0 ,0 ))[:3 ]
	pixeldata =list (im .getdata ())
	for i ,pixel in enumerate (pixeldata ):
		if pixel [:3 ]==co :
			pixeldata [i ]=(*co ,0 )
	im .putdata (pixeldata )
	return im
def img2base64 (im ,html =False ):
	with tempfile .TemporaryFile ("w+b")as f :
		im .save (f ,"PNG")
		f .seek (0 )
		imstr =f .read ()
	imb64 =base64 .b64encode (imstr )
	imb64 =str (imb64 ,encoding ='ascii')
	if html :
		return "data:image/png;base64,{}".format (imb64 )
	else :
		return imb64
def img2html (im ,**attrs ):
	return r'''<img {}src="data:image/png;base64,{}">'''.format (
	"".join ('''{}="{}" '''.format (k ,str (v ))for k ,v in attrs .items ()),
	img2base64 (im )
	)
def invert_bitmap (bitmap ):
	return ImageOps .invert (bitmap .convert ('L')).convert ('1')
try :from PySide import QtGui
except :
	try :from PyQt4 import QtGui
	except :from PyQt5 import QtGui
def bitmap2qt (bitmap ):
	im =bitmap .convert ('L')
	return QtGui .QBitmap (QtGui .QPixmap (imageqt .ImageQt (im )))
def pixmap2qt (pixmap ):
	return QtGui .QPixmap (imageqt .ImageQt (pixmap ))
def filter_rounding_bitmap (im ,blur ,ofs =0 ):
	from PIL import ImageFilter ,ImageOps
	im2 =im .convert ('L')
	if ofs >0 :
		im2 =im2 .filter (ImageFilter .MaxFilter (ofs ))
	elif ofs <0 :
		im2 =im2 .filter (ImageFilter .MinFilter (abs (ofs )))
	im2 =im2 .filter (ImageFilter .GaussianBlur (blur ))
	im2 =ImageOps .posterize (im2 ,1 )
	im2 =ImageOps .autocontrast (im2 )
	return im2 .convert ('1')
