from binkeul .betl .kode import Kode
class FKode (Kode ):
	def __new__ (cls ,value ):
		if isinstance (value ,Kode ):
			assert value .channel ==15
			return super ().__new__ (cls ,value .value ,channel =15 )
		return super ().__new__ (cls ,value ,channel =15 )
	def __init__ (self ,value ):
		pass
	def __repr__ (self ):
		return "EKode({})".format (self .value )
