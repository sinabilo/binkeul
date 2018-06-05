from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .ekode import EKode
import tempfile ,filecmp
from array import array
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_EKode_01 (self ):
		b01 =bytes ("한abhjahha022993djdad","utf8")
		t01 ,lb01 =EKode .aryFromBytes (b01 )
		eq_ (lb01 ,26 )
		eq_ (b01 ,EKode .bytesFromAry (t01 ,lb01 ))
		b02 =array ('L',[1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ]).tobytes ()
		t02 ,lb02 =EKode .aryFromBytes (b02 )
		eq_ (len (EKode .bytesFromAry (t02 ,lb02 )),len (b02 ))
		eq_ (EKode .bytesFromAry (t02 ,lb02 ),b02 )
		b03 =b""
		t03 ,lb03 =EKode .aryFromBytes (b03 )
		eq_ (EKode .bytesFromAry (t03 ,lb03 ),b"")
		eq_ (lb03 ,0 )
'''
def test_Ff_02(self):
    pass
    eq_(UvkOrd_,make_uvkord())
def test_Ff_03(self):
    pass
'''
