from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .kode import *
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		self .kd1 =Kode (514243 )
		self .kd2 =Kode (65535 )
		self .kd3 =Kode (2 **32 -1 )
	def test_Kode_01 (self ):
		eq_ (repr (self .kd1 ),'Kode(64280,29)')
		eq_ (self .kd1 .chnofs ,(29 ,3 ))
	def test_Kode_02 (self ):
		eq_ (repr (self .kd2 ),'Kode(0,15)')
		eq_ (self .kd2 .chnofs ,(15 ,17 ))
	def test_Kode_03 (self ):
		eq_ (repr (self .kd3 ),'Kode(None,-1)')
		eq_ (self .kd3 .chnofs ,(-1 ,33 ))
