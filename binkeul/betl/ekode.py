'''
'''
from array import array
from binkeul .betl .kode import Kode
class EKodeAry (array ):
	''' 30 bit 값의 배열 ,
    마지막 30bit에서 사용할 비트 값 (0,2,4,6,...30) 16 가지 유형이 필요.
    즉, 각 타입 마다 4가지 유형을 설정할 4bit flag 가 있어야 한다.
    '''
	bit30mask =int ("1"*30 ,2 )
	def __new__ (cls ,kodelist ,lastbits =30 ):
		return super ().__new__ (cls ,"L",kodelist )
	def __init__ (self ,kodelist ,lastbits =30 ):
		assert lastbits %2 ==0 and 0 <=lastbits <=30
		assert (self [-1 ]>>2 )<2 **lastbits
		self .lastbits =lastbits
	def __repr__ (self ):
		return super ().__repr__ ().replace ("array('L', ",self .__class__ .__name__ +"(")
	@classmethod
	def fromBytes (cls ,bts ):
		assert isinstance (bts ,bytes )
		ekode_ary =array ('L',[])
		bitcnt =0
		bitnum =0
		for b in bts :
			bitnum |=b <<bitcnt
			bitcnt +=8
			if bitcnt >30 :
				ekode_ary .append (EKode (bitnum &cls .bit30mask ))
				bitnum >>=30
				bitcnt -=30
		if bitcnt :
			ekode_ary .append (EKode (bitnum ))
		return EKodeAry (ekode_ary ,bitcnt )
	def toKeul (self ,fkode ):
		kl =Keul ([fkode ])
		kl .extend (self )
		return kl
	def toBytes (self ):
		bts =array ("B",[])
		bitcnt =0
		bitnum =0
		for kode in self :
			ekode =Kode .toSub (kode )
			assert ekode .channel ==30
			bitnum |=ekode .value <<bitcnt
			bitcnt +=30
			m ,n =divmod (bitcnt ,8 )
			for i in range (m ):
				bts .append (bitnum &255 )
				bitnum >>=8
			bitcnt =n
		return bts .tobytes ()
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
