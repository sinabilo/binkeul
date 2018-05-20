from nose .tools import *
import __head
from binkeul .betl .z3a2 import *
class TestSuite (__head .ClsTest ):
	def setUp (self ):
		pass
	def test_Z3A2_01 (self ):
		for x in (-256 ,65535 ,1234 ,56779 ):
			a01e =Z3a2 .pack (x )
			a01d =Z3a2 .unpack (a01e )
			eq_ (x ,a01d )
	def test_Z3A2_02 (self ):
		eq_ (Z3a2 .pack (0 ),'EA')
		eq_ (Z3a2 .pack (-256 ),'AA')
		eq_ (Z3a2 .pack (0 ,False ),'AA')
		eq_ (Z3a2 .pack (65535 ),'zzz')
		eq_ (Z3a2 .pack (65791 ,False ),'zzz')
	def test_Z3A2_03 (self ):
		with assert_raises (ZeroDivisionError ):
			45 /0
		ff =lambda :45 /0
		assert_raises (ZeroDivisionError ,ff )
		with assert_raises (AssertionError ):
			Z3a2 .pack (65536 )
		with assert_raises (AssertionError ):
			Z3a2 .pack (-1 ,False )
	def test_Z3A2_04 (self ):
		z3a2s =Z3a2 .split ("aazzzDPEA")
		eq_ (z3a2s ,['aa','zzz','DP','EA'])
		with assert_raises (AssertionError ):
			Z3a2 .split ("aazzzDPEAX",True )
		eq_ (Z3a2 .split ('aazzzDPS'),None )
	def test_Z3a2s_01 (self ):
		zts =Z3a2s ("WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAncC")
		ok_ (zts .check ())
		with assert_raises (BinkeulError ):
			Z3a2s ("WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAncC0",True )
		eq_ (str (zts .toBytes (),'utf8'),"고양이가 개 흉내를 내다")
	def test_Z3a2sIO_01 (self ):
		txt ="고양이가 개 흉내를 내다"
		bts =bytes (txt ,'utf8')
		zio =Z3a2sIO (bts )
		eq_ (zio .readAll (),"WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAncC")
		eq_ (str (zio .toBytes (),'utf8'),txt )
		zio .endWrite (b"aaa")
	def test_Z3a2sIO_02 (self ):
		txt ="고양이가 개 흉내를 내다"
		bts =bytes (txt ,'utf8')
		zio =Z3a2sIO (bts )
		bts2 =bytes ('하하하','utf8')
		eq_ (zio .readAll (),"WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAncC")
		zio .endWrite (bts2 )
		eq_ (zio .readAll (),"WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAnZgQVFwuyuZgKVFw")
		eq_ (str (zio .toBytes (),'utf8'),"고양이가 개 흉내를 내다하하하")
		zio .endWrite (b'aaa')
		eq_ (str (zio .toBytes (),'utf8'),"고양이가 개 흉내를 내다하하하aaa")
		zio .endWrite (b'aaa')
		eq_ (zio .readAll (),"WuLZEQuOLVsEyzEtyGyYIVpCZfCUueUEfZCCwQkZaGWWJuAnZgQVFwuyuZgKVFwSzcSzcSzc")
		eq_ (str (zio .toBytes (),'utf8'),"고양이가 개 흉내를 내다하하하aaaaaa")
