from datetime import date
from pathlib import Path
import os ,io
import pathlib ,pickle
from functools import lru_cache
import peewee as pw
from PIL import Image
from binkeul .base import CONF
from binkeul .betl .kode import Kode ,ForSub
from binkeul .tools import hash_file ,isurl
from binkeul .tools import pilfunc
from binkeul .betl .pubcls import Rect ,Sz ,SizeStyle ,FixStyle ,FixR
from binkeul .tools .svgimage import svgImage
db =pw .SqliteDatabase (CONF ['db-file'])
class UKodeTb (pw .Model ):
	kodeval =pw .IntegerField (primary_key =True )
	hash =pw .FixedCharField (40 ,unique =True )
	path =pw .TextField ()
	kind =pw .CharField ()
	tags =pw .TextField ()
	mday =pw .DateField ()
	data =pw .BlobField ()
	width =pw .IntegerField ()
	height =pw .IntegerField ()
	class Meta :
		database =db
	@classmethod
	def createByUrl (cls ,url ,tgs =''):
		pass
	@classmethod
	def _fdsFromFile (cls ,file ):
		hash =hash_file (file )
		kind =os .path .splitext (file )[1 ].lower ()
		path =os .path .realpath (file )
		data =Path (file ).read_bytes ()
		width ,height =cls ._get_size (kind ,data )
		assert kind in (".svg",".png",".gif",".jpg")
		return {"hash":hash ,"kind":kind ,"path":path ,"data":data ,"width":width ,"height":height }
	@classmethod
	def updateByFile (cls ,ukode ,file ,tags =''):
		kodeval =ukode .value
		q =cls .update (
		tags =tags ,
		mday =date .today (),
		**cls ._fdsFromFile (file )
		).where (cls .kodeval ==kodeval )
		return q .execute ()
	@classmethod
	def createByFile (cls ,file ,tags =''):
		q =cls .insert (
		tags =tags ,
		mday =date .today (),
		**cls ._fdsFromFile (file )
		)
		return UKode (q .execute ())
	@classmethod
	def _get_size (cls ,kind ,data ):
		import io ,re
		from PIL import Image
		from xml .etree .ElementTree import parse
		fp =io .BytesIO ()
		fp .write (data )
		fp .seek (0 )
		if kind in (".png",".gif",".jpg"):
			im =Image .open (fp )
			size =im .size
		elif kind ==".svg":
			tree =parse (fp )
			svg =tree .getroot ()
			size =tuple (
			int (re .match ("[0-9]+",g ).group (0 ))for g in
			(svg .get ("width"),svg .get ("height"))
			)
		fp .close ()
		return size
	@classmethod
	def search (cls ,word ):
		q =cls .select ().where (cls .tags .contains (word ))
		return [UKode (obj .kodeval )for obj in q ]
UKODE_CHN =CONF ['ukode-channel']
assert 10 <=UKODE_CHN <=16
class UKode (ForSub ,Kode ):
	Tb =UKodeTb
	def __new__ (cls ,value ):
		if isinstance (value ,Kode ):
			assert value .channel ==UKODE_CHN
			return super ().__new__ (cls ,value .value ,channel =UKODE_CHN )
		return super ().__new__ (cls ,value ,channel =UKODE_CHN )
	def __init__ (self ,value ):
		pass
	def __repr__ (self ):
		return "UKode({})".format (self .value )
	def getData (self ):
		r =UKodeTb .get (kodeval =self .value )
		return (r .data ,r .kind )
	def getDataB64 (self ):
		import base64
		data ,kind =self .getData ()
		bstr =base64 .b64encode (data )
		return "data:image/{};base64,{}".format (kind [1 :],str (bstr ,encoding ='ascii'))
	def getThumb (self ,unitsize =2 ,fix =FixStyle .square ):
		bytes ,kind =self .getData ()
		if kind ==".svg":
			bytes =svgImage (bytes )
		bts =io .BytesIO ()
		bts .write (bytes )
		bts .seek (0 )
		im =Image .open (bts )
		size =self .rect .fixRect (fix ).scRect (unitsize ).size
		rim =im .resize (size ).convert ('RGBA')
		if kind ==".svg":
			rim =pilfunc .set_alpha (rim )
		return rim
	def getFile (self ):
		r =UKodeTb .get (kodeval =self .value )
		return None if isurl (r .path )else r .path
	def getUrl (self ):
		r =UKodeTb .get (kodeval =self .value )
		if isurl (r .path ):
			return r .path
		else :
			import pathlib
			return pathlib .Path (r .path ).as_uri ()
	def getSize (self ,style =SizeStyle .pic2x ):
		UFixSz =60
		UFixWh =60 *60
		FixSz =FixR *2
		r =UKodeTb .get (kodeval =self .value )
		size =Sz (r .width ,r .height )
		if style ==SizeStyle .orign :
			return size
		tofix =lambda sz :int (sz *(FixSz /UFixSz ))
		w ,h =size
		if w >UFixSz or h >UFixSz :
			rate =pow ((w *h )/UFixWh ,0.5 )
			w =w /rate
			h =h /rate
		w =tofix (w )
		h =tofix (h )
		size =Sz (FixSz if w >FixSz else w ,
		FixSz if h >FixSz else h )
		if style ==SizeStyle .pic1x :
			return size
		elif style ==SizeStyle .pic2x :
			return Sz (size .w *2 ,size .h *2 )
	@lru_cache (maxsize =None )
	def getRect (self ,style =SizeStyle .pic2x ):
		width ,height =self .getSize (style )
		w2 ,h2 =int (width /2 ),int (height /2 )
		return Rect (-w2 ,-h2 ,width -w2 ,height -h2 )
	@property
	def rect (self ):
		return self .getRect (style =SizeStyle .pic1x )
	def texts (self ):
		r =self .Tb .get (kodeval =self .value )
		return r .tags
