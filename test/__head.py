'''
실행하기
=====================
    $ nosetest3
'''
from nose .tools import *
from binkeul .tools import godir ,tmfopen
import re ,os ,sys ,io
def getsatic (_file_ ):
	'''
    현재 디렉토리와 test 작업 디렉토리를 구한다.
    ::
        getsatic(__file__)
    godir 와 함께 사용할 때는
    반드시 setup_class, teardown_class 에서 쌍으로 사용할 것
    ::
        @classmethod
        def setup_class(klass):
            godir(getsatic(__file__))
        @classmethod
        def teardown_class(klass):
            godir()
    '''
	path =os .path .splitext (os .path .abspath (_file_ ))[0 ]
	l ,p ,r =path .rpartition ('test-')
	if p =='':
		l ,p ,r =path .rpartition ('t-')
	stdir =os .path .join (l ,"static",r )
	return stdir
class ClsTest :
	'''
    def test_1(self):
        eq_(2*2,4)
    def test_2(self):
        ok_(30+60 == 90 )
    #@nottest
    @istest
    def o3(self):
        eq_(2*2,4)
    '''
	@classmethod
	def setup_class (klass ):
		"""This method is run once for each class before any tests are run"""
	@classmethod
	def teardown_class (klass ):
		"""This method is run once for each class _after_ all tests are run"""
	def setUp (self ):
		"""This method is run once before _each_ test method is executed"""
	def teardown (self ):
		"""This method is run once after _each_ test method is executed"""
