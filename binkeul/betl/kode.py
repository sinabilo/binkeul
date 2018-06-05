import struct
from binkeul .betl .z3a2 import Z3a2
from functools import lru_cache
class ForSub ():
	def __getnewargs__ (self ):
		return (self .value ,)
	def inTable (self ):
		tb =self .Tb
		q =tb .select ().where (tb .kodeval ==self .value )
		return True if q else False
	def get (self ,attr ):
		assert self .Tb
		r =self .Tb .get (kodeval =self .value )
		return getattr (r ,attr )
	@classmethod
	def sample (cls ,count =1 ):
		from peewee import fn
		query =cls .Tb .select ().order_by (fn .Random ()).limit (count )
		for obj in query .objects ():
			yield cls (obj .kodeval )
	@classmethod
	def all (cls ):
		query =cls .Tb .select ()
		for obj in query .objects ():
			yield cls (obj .kodeval )
	def texts (self ):
		raise NotImplementedError ()
class Kode (int ):
	def __new__ (cls ,value ,channel =None ):
		if channel ==None :
			return super ().__new__ (cls ,value )
		assert -1 <=channel <32
		if channel ==-1 :
			assert value ==None
			value =0
		else :
			assert value .bit_length ()<=channel
		bitofs =32 -channel
		chbits =(1 <<(31 -channel ))-1
		return super ().__new__ (
		cls ,
		(value <<bitofs )|chbits
		)
	def __deepcopy__ (self ,memo ):
		import copy
		return Kode .toSub (int (self ))
	def __copy__ (self ,memo =None ):
		import copy
		return Kode .toSub (int (self ))
	def __init__ (self ,value ,channel =None ):
		pass
	@staticmethod
	def toSub (number ):
		from binkeul .betl .bkode import BKode
		from binkeul .betl .solnode import SKode
		from binkeul .betl .ukode import UKode ,UKODE_CHN
		kode =Kode (number )
		from binkeul .betl .ekode import EKode
		from binkeul .betl .fkode import FKode
		ktype ={
		31 :BKode ,
		30 :EKode ,
		UKODE_CHN :UKode ,
		15 :FKode ,
		2 :SKode ,
		0 :SKode ,
		}.get (kode .channel )
		return ktype (kode )if ktype else kode
	@staticmethod
	def GetChnOfs (number ):
		bs =number ^(number +1 )
		ofs =bs .bit_length ()
		return (32 -ofs ,ofs )
	@property
	def chnofs (self ):
		return Kode .GetChnOfs (self )
	@property
	def bitofs (self ):
		return Kode .GetChnOfs (self )[1 ]
	@property
	def channel (self ):
		return Kode .GetChnOfs (self )[0 ]
	@property
	def value (self ):
		chn ,ofs =Kode .GetChnOfs (self )
		if chn ==-1 :
			return None
		return self .numerator >>ofs
	def __repr__ (self ):
		return "Kode({},{})".format (self .value ,self .channel )
	@classmethod
	def fromBytes (cls ,bts ):
		num =struct .unpack ("<L",bts )[0 ]
		return cls .toSub (num )
	def toBytes (self ):
		return struct .pack ("<L",self .numerator )
	@classmethod
	def fromZ3a2s (cls ,zts ):
		za1 ,za2 =Z3a2 .split (zts )
		num =Z3a2 .unpack (za1 )+(Z3a2 .unpack (za2 )<<16 )
		return cls .toSub (num )
	@lru_cache (maxsize =None )
	def toZ3a2s (self ):
		num =self .numerator
		return Z3a2 .pack (num &65535 )+Z3a2 .pack (num >>16 )
	def uniqName (self ):
		za =self .toZ3a2s ()
		num =0
		for i ,ap in enumerate (za ):
			if ap .isupper ():
				num |=(1 <<i )
		return za +str (num )
