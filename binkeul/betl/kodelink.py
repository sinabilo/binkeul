from collections import defaultdict
class KodeLink :
	_kodelink =defaultdict (set )
	def __init__ (self ):
		pass
	def link (self ,pkode ,kode ):
		self ._kodelink [pkode ].add (kode )
	def islink (self ,pkode ,kode ):
		return kode in self ._kodelink [pkode ]
