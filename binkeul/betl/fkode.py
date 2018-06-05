from binkeul .betl .kode import Kode
from binkeul .betl .keul import Keul
from binkeul .betl .ekode import EKode
from enum import IntEnum
class Ekind (IntEnum ):
	__min__ =0
	Binary =1
	String =2
	Number =3
	MNumber =4
	__max__ =5
class FKode (Kode ):
	def __new__ (cls ,value ):
		if isinstance (value ,Kode ):
			assert value .channel ==15
			return super ().__new__ (cls ,value .value ,channel =15 )
		return super ().__new__ (cls ,value ,channel =15 )
	def __init__ (self ,value ):
		pass
	def __repr__ (self ):
		return "FKode({})".format (self .value )
	@property
	def lastbits (self ):
		return (self .value &0b1111 )<<1
	@property
	def ekind (self ):
		return self .value >>4
	@classmethod
	def createFKode (cls ,ekind ,lastbits ):
		assert lastbits %2 ==0 and 0 <=lastbits <=30
		assert Ekind .__min__ <ekind <Ekind .__max__
		return cls ((ekind <<4 )|(lastbits >>1 ))
	@classmethod
	def keulFromData (cls ,data ):
		if isinstance (data ,bytes ):
			ekind =Ekind .Binary
			edata =data
		elif isinstance (data ,str ):
			ekind =Ekind .String
			edata =bytes (data ,'utf8')
		elif isinstance (data ,int ):
			if data <0 :
				ekind =Ekind .MNumber
				data =(~data )
			else :
				ekind =Ekind .Number
			nbit =data .bit_length ()
			nByte =(nbit //8 )+(1 if nbit %8 else 0 )
			edata =data .to_bytes (nByte ,'big')
		kode_ary ,lastbits =EKode .aryFromBytes (edata )
		kode_ary .insert (0 ,cls .createFKode (ekind ,lastbits ))
		return Keul (kode_ary )
	@classmethod
	def dataFromKeul (cls ,keul ):
		fkode =Kode .toSub (keul [0 ])
		ekode_ary =keul [1 :]
		bts =EKode .bytesFromAry (ekode_ary ,fkode .lastbits )
		if fkode .ekind ==Ekind .Binary :
			return bts
		elif fkode .ekind ==Ekind .String :
			return str (bts ,"utf8")
		elif fkode .ekind ==Ekind .Number :
			return int .from_bytes (bts ,"big")
		elif fkode .ekind ==Ekind .MNumber :
			return ~(int .from_bytes (bts ,"big"))
