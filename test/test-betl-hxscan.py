from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from PIL import Image
from binkeul .betl .hx import Hx ,HxSet
from binkeul .betl .hxscan import HxScanner
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	@classmethod
	def setup_class (klass ):
		godir (getsatic (__file__ ))
	@classmethod
	def teardown_class (klass ):
		godir ()
	def setUp (self ):
		pass
	def test_HxScan_01 (self ):
		hxs1 =HxSet ('0011010000000100010010000000011000011110011000000000000000000000000000111110011111011100011111001')
		im =Image .open ("hxbmp01.png")
		hxs2 =HxScanner .read (im )
		eq_ (hxs1 ,hxs2 )
