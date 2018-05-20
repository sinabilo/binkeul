from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .bkode import *
from binkeul .betl .kode import Kode
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_BKode_01 (self ):
		a =BKodeTb .getBKode (HxSet ('0000000000000000000000001110011000000100000010010010000000000000000001110100101000011100001011011'))
		b =BKode (1007507256 )
		c =Kode (1007507256 ,31 )
		d =2015014512
		ok_ (a ==b ==c ==d )
	def test_BKode_02 (self ):
		eq_ (repr (Kode .toSub (2015014512 )),'BKode(1007507256)')
	def test_BKode_03 (self ):
		a =BKodeTb .getHxs (BKode (1007507256 ))
		b =HxSet ({0 ,1 ,3 ,4 ,6 ,11 ,12 ,13 ,18 ,20 ,23 ,25 ,26 ,27 ,46 ,49 ,52 ,59 ,66 ,67 ,70 ,71 ,72 })
		eq_ (a ,b )
		c =BKodeTb .getBKode (b )
		eq_ (BKode (1007507256 ),c )
	def test_BKode_04 (self ):
		hxs =HxSet ({0 ,3 ,4 ,6 ,7 ,11 ,12 ,13 ,16 ,17 ,18 ,19 ,22 ,23 ,24 ,25 })
		bx =hxs .getBx ()
		bkode =BKode (bx <<2 )
		eq_ (bkode .centerHxs (),hxs )
	def test_BKode_05 (self ):
		bkode1 =BKode (1168011696 )
		z1 =bkode1 .toZ3a2s ()
		eq_ (z1 ,'yhCUyE')
		eq_ (Kode .fromZ3a2s (z1 ),BKode (1168011696 ))
	def test_BKode_05 (self ):
		bkode1 =BKode (1865030684 )
		bts1 =bkode1 .toBytes ()
		eq_ (bts1 ,b'88T\xde')
		eq_ (Kode .fromBytes (bts1 ),BKode (1865030684 ))
	def test_BKode_06 (self ):
		import pickle ,copy
		b =BKode (26939096 )
		dump =pickle .dumps (b )
		b2 =pickle .loads (dump )
		eq_ (repr (b2 ),"BKode(26939096)")
		b3 =copy .copy (b )
		eq_ (repr (b3 ),"BKode(26939096)")
		b4 =copy .deepcopy (b )
		eq_ (repr (b4 ),"BKode(26939096)")
	def test_BKode_06 (self ):
		for b in BKode .all ():
			eq_ (b .rect ,b .getHxs ().rect )
