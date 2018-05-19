from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .qkui .fodata import *
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		a =Fodraw ([0 ,9 ,8 ,7 ,6 ,5 ])
		b =Fodraw ([1 ,2 ,3 ,4 ,5 ])
		c =Fodraw ([10 ,11 ,12 ,5 ,13 ])
		fodraw_stack =FodrawStack ()
		fodraw_stack .addItem (a )
		fodraw_stack .addItem (b )
		fodraw_stack .addItem (c )
		self .fodraw_stack =fodraw_stack
	def test_FoData_01 (self ):
		eq_ (self .fodraw_stack .allw (),
		Fodraw ({0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 }))
		eq_ (self .fodraw_stack .sumw (),
		Fodraw ({0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 }))
	def test_FoData_02 (self ):
		self .fodraw_stack .undo ()
		eq_ (self .fodraw_stack .allw (),
		Fodraw ({0 ,1 ,2 ,3 ,4 ,6 ,7 ,8 ,9 }))
		eq_ (self .fodraw_stack .sumw (),
		Fodraw ({0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 }))
	def test_FoData_03 (self ):
		self .fodraw_stack .undo ()
		self .fodraw_stack .undo ()
		eq_ (self .fodraw_stack .allw (),Fodraw ({0 ,5 ,6 ,7 ,8 ,9 }))
		self .fodraw_stack .redo ()
		eq_ (self .fodraw_stack .allw (),Fodraw ({0 ,1 ,2 ,3 ,4 ,6 ,7 ,8 ,9 }))
	def test_FoData_04 (self ):
		fodraw3_stack =FodrawStack ()
		for i in range (15 ):
			fodraw3_stack .addItem (Fodraw ([i ]))
		eq_ (fodraw3_stack .allw (),
		Fodraw ({0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 }))
