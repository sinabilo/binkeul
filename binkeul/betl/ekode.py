'''
'''
from array import array
from binkeul .betl .kode import Kode
class EKode (Kode ):
	def __new__ (cls ,value ):
		if isinstance (value ,Kode ):
			assert value .channel ==30
			return super ().__new__ (cls ,value .value ,channel =30 )
		return super ().__new__ (cls ,value ,channel =30 )
	def __init__ (self ,value ):
		pass
	def __repr__ (self ):
		return "EKode({})".format (self .value )
	bit30mask =int ("1"*30 ,2 )
	@classmethod
	def aryFromBytes (cls ,bts ):
		assert isinstance (bts ,bytes )
		ekode_ary =array ('L',[])
		bitcnt =0
		bitnum =0
		for b in bts :
			bitnum |=b <<bitcnt
			bitcnt +=8
			if bitcnt >30 :
				ekode_ary .append (cls (bitnum &cls .bit30mask ))
				bitnum >>=30
				bitcnt -=30
		if bitcnt :
			ekode_ary .append (cls (bitnum ))
		lastbits =bitcnt
		return ekode_ary ,lastbits
	@classmethod
	def bytesFromAry (cls ,ekode_ary ,lastbits ):
		bts =array ("B",[])
		if len (ekode_ary )==0 :
			return b''
		bitcnt =0
		bitnum =0
		for kode in ekode_ary :
			ekode =Kode .toSub (kode )
			assert ekode .channel ==30
			bitnum |=ekode .value <<bitcnt
			bitcnt +=30
			m ,n =divmod (bitcnt ,8 )
			for i in range (m ):
				bts .append (bitnum &255 )
				bitnum >>=8
			bitcnt =n
		rbits =(30 -bitcnt )-lastbits
		rB ,n0 =divmod (rbits ,8 )
		assert n0 ==0
		bts =bts [:-rB ]if rB else bts
		return bts .tobytes ()
