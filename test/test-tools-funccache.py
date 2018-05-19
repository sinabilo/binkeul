from nose .tools import *
import __head
from binkeul .tools .cachefunc import fcached
from binkeul .betl .ukode import UKode
addnum =0
class WKode (UKode ):
	@fcached ()
	def area (self ):
		global addnum
		return self .rect .width *self .rect .height +addnum
class TestSuite (__head .ClsTest ):
	def setUp (self ):
		pass
	def test_PCACHE_01 (self ):
		global addnum
		eq_ (WKode (1 ).area (cache_update =True ),400 )
		addnum =10000
		eq_ (WKode (1 ).area (),400 )
		eq_ (WKode (1 ).area (cache_update =True ),10400 )
		eq_ (WKode (1 ).area (),10400 )
		eq_ (WKode (5 ).area (cache_update =True ),10340 )
