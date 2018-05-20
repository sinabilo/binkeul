'''
nosetests n01.py
nosetests -v n01.py
nose2
nose2 -v
'''
from nose .tools import eq_ ,ok_ ,nottest ,istest
def test_sum ():
	eq_ (2 +2 ,4 )
def test_sum2 ():
	ok_ (2 +2 ==4 ,"Expected failure")
@nottest
def test_failing_sum ():
	ok_ (2 +2 ==4 ,"Expected failure")
def test_subs ():
	ok_ ("Unexpected failure",6 -2 ==4 )
class TestSuite :
	def test_mult (self ):
		eq_ (2 *2 ,4 )
	@istest
	def oop_te_mm (self ):
		eq_ (2 *2 ,4 )
