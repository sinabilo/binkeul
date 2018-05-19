from nose .tools import *
from __head import ClsTest ,godir ,getsatic ,tmfopen
from PIL import Image
from binkeul .betl .hx import Hx ,HxSet
from binkeul .betl .hxplot import HxPlotFrm
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
		self .hxs1 =HxSet ('0011010000000100010010000000011000011110011000000000000000000000000000111110011111011100011111001')
		self .plotter1 =HxPlotFrm (1 )
		self .plotter2 =HxPlotFrm (2 )
	def test_HxDraw_01 (self ):
		with tmfopen (suffix ='.png')as tf :
			wim1 =self .plotter1 .draw (self .hxs1 )
			wim1 .save (tf ,'png')
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"hxbmp01.png"))
	def test_HxDraw_02 (self ):
		with tmfopen (suffix ='.png')as tf :
			wim2 =self .plotter2 .draw (self .hxs1 )
			wim2 .save (tf ,'png')
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"hxbmp02.png"))
