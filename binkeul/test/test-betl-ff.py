from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .ffv import FfvSet
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_Ff_01 (self ):
		v01 =604266026
		t01 =FfvSet (v01 )
		eq_ (t01 .bitls ,[0 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,1 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ])
		t01 .bitls [4 ]^=1
		t02 =FfvSet .fromBitSet (t01 .bitls )
		eq_ (t02 .bitls ,FfvSet (v01 ).bitls )
		eq_ (t02 ,t01 )
		eq_ (t02 .data ,v01 )
'''
def test_Ff_02(self):
    pass
    eq_(UvkOrd_,make_uvkord())
def test_Ff_03(self):
    pass
'''
