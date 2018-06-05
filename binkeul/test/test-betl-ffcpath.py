from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .ffcpath import FfcPath
from binkeul .betl .ffc import FfcSet
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		pass
	def test_FfcPath_01 (self ):
		ffcs01 =FfcSet (1562579265 )
		ffcp01 =FfcPath (ffcs01 )
		eq_ (ffcp01 .getPathd (),
		'''M-5 5-5 3-1 3-1 1 3 1 3-1 5-1 5 1 3 1 3 3 5 3 5 9 1 9 1 7 3 7 3 3 1 3 1 5zM 1-9 3-9 3-7 5-7 5-5 3-5 3-7 1-7 1-5-1-5-1-7-5-7-5-9-1-9-1-7 1-7zM-3-3-1-3-1-1-3-1-3 1-5 1-5-1-3-1z''')
		eq_ (ffcp01 .getPathd (rotate =True ),
		"""M-5-5-3-5-3-1-1-1-1 3 1 3 1 5-1 5-1 3-3 3-3 5-9 5-9 1-7 1-7 3-3 3-3 1-5 1zM 9 1 9 3 7 3 7 5 5 5 5 3 7 3 7 1 5 1 5-1 7-1 7-5 9-5 9-1 7-1 7 1zM 3-3 3-1 1-1 1-3-1-3-1-5 1-5 1-3z""")
'''
def test_Ffv_02(self):
    pass
    eq_(UvkOrd_,make_uvkord())
def test_Ffv_03(self):
    pass
'''
