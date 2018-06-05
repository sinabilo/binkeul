from binkeul .betl .kode import *
from binkeul .betl .z3a2 import *
from binkeul .excepts import *
from binkeul .betl .pubcls import FixStyle
import array ,io ,struct ,types
class Keul (array .array ):
	def __new__ (cls ,kodes =[]):
		if isinstance (kodes ,bytes ):
			return Keul .fromBytes (kodes )
		elif isinstance (kodes ,str ):
			return Keul .fromZ3a2s (kodes )
		elif isinstance (kodes ,(list ,tuple ,array .array ,types .GeneratorType )):
			return super ().__new__ (cls ,'L',kodes )
		else :
			raise ValueError ()
	def __init__ (self ,kodes =[]):
		super ().__init__ ()
	def __iter__ (self ):
		for k in super ().__iter__ ():
			yield Kode .toSub (k )
	def __getitem__ (self ,key ):
		if isinstance (key ,int ):
			return Kode .toSub (super ().__getitem__ (key ))
		elif isinstance (key ,slice ):
			return Keul (super ().__getitem__ (key ))
		else :
			raise TypeError ("Invalid argument type.")
	def __repr__ (self ):
		zts =self .toZ3a2s ()
		return "Keul('{}')".format (
		zts [:30 ]+"..."if len (zts )>30 else zts
		)
	def getSvgItem (self ,fix =FixStyle .square ):
		pass
		return
	def toBytes (self ,getio =False ):
		kbio =io .BytesIO ()
		for x in self :
			kbio .write (struct .pack ("L",x ))
		if getio :
			return kbio
		else :
			kbio .seek (0 )
			return kbio .read ()
	def toZ3a2s (self ):
		kzio =io .StringIO ()
		for x in self :
			kzio .write (Z3a2 .pack (x &65535 )+Z3a2 .pack (x >>16 ))
		kzio .seek (0 )
		return Z3a2s (kzio .read ())
	@staticmethod
	def fromBytes (bts ):
		kl =Keul ()
		btsio =bts if isinstance (bts ,io .BytesIO )else io .BytesIO (bts )
		while 1 :
			bt1 =btsio .read (4 )
			if not bt1 :break
			num =struct .unpack ('L',bt1 )[0 ]
			kl .append (num )
		return kl
	@staticmethod
	def fromZ3a2s (zts ):
		if type (zts )==str :
			zts =Z3a2s (zts )
		return Keul .fromBytes (zts .toBytes ())
	def getSet (self ):
		return set (self )
	@classmethod
	def sample (cls ,count ):
		from binkeul .betl .bkode import BKode
		from binkeul .betl .ukode import UKode
		import random
		bkodes =list (BKode .sample (count ))
		ukodes =list (UKode .sample (count ))
		return cls (random .sample (bkodes +ukodes ,count ))
class BKeul (Keul ):
	def getHxsList (self ):
		return
	@classmethod
	def sample (cls ,count ):
		from binkeul .betl .bkode import BKode
		import random
		return cls (BKode .sample (count ))
class UKeul (Keul ):
	@classmethod
	def sample (cls ,count ):
		from binkeul .betl .ukode import UKode
		import random
		return cls (UKode .sample (count ))
