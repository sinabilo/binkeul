import peewee as pw
from datetime import date
from binkeul .base import CONF
from binkeul .betl .hx import HxMap ,HxSet
from binkeul .betl .hxpath import HxPath
from binkeul .betl .kode import Kode ,ForSub
from binkeul .betl .pubcls import Rect
from functools import lru_cache
import pickle
db =pw .SqliteDatabase (CONF ['db-file'])
class BKodeTb (pw .Model ):
	kodeval =pw .IntegerField (primary_key =True )
	hxbitset =pw .FixedCharField (97 ,unique =True )
	rect =pw .BlobField ()
	pathd =pw .TextField ()
	kind =pw .IntegerField ()
	mday =pw .DateField ()
	dics =pw .TextField ()
	tempKode ={}
	class Meta :
		database =db
		indexes =(('hxbitset',True ))
	@classmethod
	def getBKode (cls ,hxs ):
		q =cls .select ().where (cls .hxbitset ==hxs .bitset )
		if q :
			return BKode (q .get ().kodeval )
	@classmethod
	def getNew (cls ,hxs ):
		assert not cls .existHxs (hxs )
		for bkode in BKode .getBx4 (hxs ):
			if not bkode .inTable ():
				return bkode
		return None
	@classmethod
	def findMatch (cls ,hxs ,hxs_alpha ,limit ):
		def sameBtisets (hxs ):
			if len (hxs )==0 :
				return []
			bitsets =[hxs .bitset ]
			return bitsets +[HxSet (hxs ^set ([h ])).bitset for h in range (97 )]
		if not hxs_alpha :return []
		same_bitsets =sameBtisets (hxs )
		bkode_list =[]
		for r in cls .select (cls .kodeval ,cls .hxbitset ):
			if len (bkode_list )>=limit :
				break
			if r .hxbitset in same_bitsets :
				bkode_list .insert (0 ,BKode (r .kodeval ))
			elif int (r .hxbitset ,2 )&hxs_alpha .bitnum ==hxs .bitnum :
				bkode_list .append (BKode (r .kodeval ))
		return bkode_list
	@classmethod
	def getHxs (cls ,bkode ):
		q =cls .select ().where (cls .kodeval ==bkode .value )
		if q :
			return HxSet (cls .get (kodeval =bkode .value ).hxbitset )
	@classmethod
	def existHxs (cls ,hxs ):
		assert isinstance (hxs ,HxSet )
		selhxs =cls .select ().where (cls .hxbitset ==hxs .bitset )
		if selhxs .count ()==1 :
			return True
		elif selhxs .count ()==0 :
			return False
		elif selhxs .count ()>1 :
			raise ValueError ("BKodeTb 에 중복된 hxs")
	@classmethod
	def updateHxs (cls ,hxs ,bkode =None ,dics ='',kind =0 ):
		if cls .existHxs (hxs )==True :
			it =cls .get (cls .hxbitset ==hxs .bitset )
			it .delete_instance ()
		if bkode ==None :
			bks =BKode .getBx4 (hxs )
			for bkode in bks :
				selbk =cls .select ().where (cls .kodeval ==bkode .value )
				if selbk .count ()==0 :
					break
			else :
				return False
		hxp =HxPath (hxs )
		pathd =hxp .getPathd (simple =True )
		rect =repr (hxp .mgrect )
		return cls .create (kodeval =bkode .value ,hxbitset =hxs .bitset ,rect =rect ,pathd =pathd ,kind =kind ,mday =date .today (),dics =dics )
	@classmethod
	def search (cls ,word ):
		q =cls .select ().where (cls .dics .contains (word ))
		return [BKode (obj .kodeval )for obj in q ]
class BKode (ForSub ,Kode ):
	Tb =BKodeTb
	def __new__ (cls ,value ):
		if isinstance (value ,Kode ):
			assert value .channel ==31
			return super ().__new__ (cls ,value .value ,channel =31 )
		return super ().__new__ (cls ,value ,channel =31 )
	def __init__ (self ,value ):
		pass
	def __repr__ (self ):
		return "BKode({})".format (self .value )
	@property
	def kind (self ):
		return int (BKodeTb .get_or_none (kodeval =self .value ).kind )
	def getHxs (self ):
		hxs =BKodeTb .getHxs (self )
		if hxs :
			return hxs
		else :
			return self .centerHxs ()
	def centerHxs (self ):
		bx =self .bxval
		return HxSet ({
		(28 -i )
		for i in range (bx .bit_length ())
		if bx &(1 <<i )
		})
	@property
	def bxval (self ):
		return self .numerator >>3
	@classmethod
	def getBx4 (cls ,hxs ):
		bx =hxs .getBx ()
		bx <<=2
		return map (BKode ,(bx ,bx |1 ,bx |2 ,bx |3 ))
	@property
	def rect (self ):
		if self .inTable ():
			return eval (self .get ("rect"))
		else :
			hxp =HxPath (self .getHxs ())
			return hxp .mgrect
	@property
	def pathd (self ):
		if self .inTable ():
			return self .get ("pathd")
		else :
			return HxPath (self .getHxs ()).getPathd (simple =True )
	def texts (self ,keys =CONF ["dics-default"]):
		r =BKodeTb .get (kodeval =self .value )
		dics =eval (r .dics )
		text =''
		for k in keys :
			dic =dics .get (k ,None )
			if dic :
				text +="[{}] {} ".format (k ,dic )
		return text
