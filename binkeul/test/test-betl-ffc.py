from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .ffc import FfcSet
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_Ffc_01 (self ):
		v01 =604266026
		t01 =FfcSet (v01 )
		eq_ (t01 .bitls ,[0 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,1 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ])
		t01 .bitls [4 ]^=1
		t02 =FfcSet .fromBitSet (t01 .bitls )
		eq_ (t02 .bitls ,FfcSet (v01 ).bitls )
		eq_ (t02 ,t01 )
		eq_ (t02 .data ,v01 )
'''
def test_Ffv_02(self):
    pass
    eq_(UvkOrd_,make_uvkord())
def test_Ffv_03(self):
    pass
'''
