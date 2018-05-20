from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .ukode import *
from binkeul .betl .kode import Kode
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_UKode_01 (self ):
		import pickle ,copy
		b =UKode (123 )
		dump =pickle .dumps (b )
		b2 =pickle .loads (dump )
		eq_ (repr (b2 ),"UKode(123)")
		b3 =copy .copy (b )
		eq_ (repr (b3 ),"UKode(123)")
		b4 =copy .deepcopy (b )
		eq_ (repr (b4 ),"UKode(123)")
