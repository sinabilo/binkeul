class BinkeulError (Exception ):
	pass
class BkError (Exception ):
	def __init__ (self ,value ):
		self .value =value
	def __str__ (self ):
		return repr (self .value )
class BkReadError (Exception ):
	def __init__ (self ,value ):
		self .value =value
	def __str__ (self ):
		return repr (self .value )
