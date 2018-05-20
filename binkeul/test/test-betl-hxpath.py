from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from PIL import Image
from binkeul .betl .hx import Hx ,HxSet
from binkeul .betl .hxpath import HxPath
import tempfile ,filecmp
import os ,re
def path_eq (path1 ,path2 ):
	''' 두 개의 svg path 의 d 값이 동일한 도형을 나타내는지 확인. 동일하면 True
    ::
        # path2list  기능
        ss = "M-3-3-3-1-1-1-1-3zM 3 9 3 5 0 5-3 8-3 9-5 9-5 7-4 7-2 5-5 5-5 2-7 4-7 5-9 5-9 3-8 3-5 0-5-3-9-3-9-5 5-5 5 1-3 1-3 3 7 3 7-1 9-1 9 9 7 9 7 5 5 5 5 9zM 3-3 1-3 1-1 3-1z"
        x = [ re.findall( "-?[0-9]+" ,m ) for m in re.findall("(?<=M)[-0-9 ]+(?=z)",ss)]
        print(m)
    '''
	path2list =lambda pathd :[re .findall ("-?[0-9]+",m )for m in re .findall ("(?<=M)[-0-9 ]+(?=z)",pathd )]
	plist1 =path2list (path1 )
	plist2 =path2list (path2 )
	while True :
		if not plist1 :break
		pts =plist1 .pop ()
		ropts =pts
		for _ in range (len (pts )):
			if ropts in plist2 :
				plist2 .remove (ropts )
				break
			ropts =ropts [1 :]+ropts [:1 ]
		else :
			return False
	if plist1 ==plist1 ==[]:
		return True
class TestSuite (ClsTest ):
	@classmethod
	def setup_class (klass ):
		pass
	@classmethod
	def teardown_class (klass ):
		pass
	def setUp (self ):
		self .hxs1 =HxSet ({0 ,3 ,4 ,10 ,11 ,12 ,13 ,14 ,16 ,17 ,18 ,21 ,22 ,23 ,25 ,26 ,28 ,31 ,32 ,51 ,53 ,54 })
		self .hxs2 =HxSet ({0 ,3 ,4 ,5 ,6 ,7 ,11 ,12 ,13 ,15 ,16 ,17 ,18 ,19 ,22 ,23 ,24 ,25 ,26 ,54 ,55 ,58 ,59 ,60 ,61 ,66 ,67 ,76 ,79 ,83 ,91 ,93 ,94 })
		self .hxs3 =HxSet ({0 ,1 ,2 ,4 ,6 ,8 ,9 ,11 ,13 ,16 ,18 ,20 ,21 ,23 ,25 ,27 ,28 ,46 ,49 ,52 ,57 ,59 ,61 ,64 ,66 ,68 ,73 ,76 ,79 })
		self .hxp1 =HxPath (self .hxs1 )
		self .hxp2 =HxPath (self .hxs2 )
	def test_HxPath_01 (self ):
		pass
	def test_HxPath_10 (self ):
		pathd1 ='M 0 5-1 5-2 5-3 5-4 5-5 5-5 4-5 3-4 3-3 2-2 1-3 1-4 1-5 1-5 0-5-1-4-1-3-2-2-3-3-3-4-3-5-3-5-4-5-5-5-6-5-7-5-8-5-9-4-9-3-9-3-8-3-7-3-6-3-5-2-5-1-5 0-5 1-5 1-4 1-3 0-3-1-2-2-1-1-1 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 9 0 9 1 8 1 7 2 6 3 5 4 5 5 4 5 3 5 2 5 1 5zM 2 3 3 3 3 2 3 1 2 1 1 1 1 2 1 3zM 6 1 5 1 5 2zM-1 2-2 3-1 3z'
		ok_ (path_eq (self .hxp1 .getPathd (simple =False ),pathd1 ))
		pathd1s ='M-5 5-5 3-4 3-2 1-5 1-5-1-4-1-2-3-5-3-5-9-3-9-3-5 1-5 1-3 0-3-2-1 9-1 9 1 8 1 5 4 5 5zM 3 3 3 1 1 1 1 3zM 6 1 5 1 5 2zM-1 2-2 3-1 3z'
		ok_ (path_eq (self .hxp1 .getPathd (simple =True ),pathd1s ))
	def test_HxPath_11 (self ):
		pathd2 ='M-2-3-3-3-3-2-3-1-2-1-1-1-1-2-1-3zM 4 9 3 9 3 8 3 7 3 6 3 5 2 5 1 5 0 5-1 6-2 7-3 8-3 9-4 9-5 9-5 8-5 7-4 7-3 6-2 5-3 5-4 5-5 5-5 4-5 3-5 2-6 3-7 4-7 5-8 5-9 5-9 4-9 3-8 3-7 2-6 1-5 0-5-1-5-2-5-3-6-3-7-3-8-3-9-3-9-4-9-5-8-5-7-5-6-5-5-5-4-5-3-5-2-5-1-5 0-5 1-5 2-5 3-5 4-5 5-5 5-4 5-3 5-2 5-1 5 0 5 1 4 1 3 1 2 1 1 1 0 1-1 1-2 1-3 1-3 2-3 3-2 3-1 3 0 3 1 3 2 3 3 3 4 3 5 3 6 3 7 3 7 2 7 1 7 0 7-1 8-1 9-1 9 0 9 1 9 2 9 3 9 4 9 5 9 6 9 7 9 8 9 9 8 9 7 9 7 8 7 7 7 6 7 5 6 5 5 5 5 6 5 7 5 8 5 9zM 3-3 2-3 1-3 1-2 1-1 2-1 3-1 3-2z'
		ok_ (path_eq (self .hxp2 .getPathd (simple =False ),pathd2 ))
		pathd2s ='M-3-3-3-1-1-1-1-3zM 3 9 3 5 0 5-3 8-3 9-5 9-5 7-4 7-2 5-5 5-5 2-7 4-7 5-9 5-9 3-8 3-5 0-5-3-9-3-9-5 5-5 5 1-3 1-3 3 7 3 7-1 9-1 9 9 7 9 7 5 5 5 5 9zM 3-3 1-3 1-1 3-1z'
		ok_ (path_eq (self .hxp2 .getPathd (simple =True ),pathd2s ))
	def test_HxPath_21 (self ):
		self .hxp2 .remove (self .hxs3 )
		ok_ (path_eq (self .hxp2 .getPathd (simple =True ),'M-3-3-3-1-1-1-1-3zM 3 9 3 5 1 5 1 3 3 3 3 5 5 5 5 3 7 3 7-1 9-1 9 3 7 3 7 5 9 5 9 7 7 7 7 5 5 5 5 9zM-5 7-4 7-2 5-3 5-3 3-5 3-5 1-3 1-3-1-5-1-5-3-7-3-7-5-5-5-5-3-3-3-3-5-1-5-1-3 1-3 1-5 3-5 3-3 5-3 5-1 3-1 3 1 1 1 1-1-1-1-1 1-3 1-3 3-1 3-1 4 0 4 0 5-3 8-3 9-5 9zM 3-3 1-3 1-1 3-1z'))
	def test_HxPath_22 (self ):
		self .hxp2 .update (self .hxs3 )
		ok_ (path_eq (self .hxp2 .getPathd (simple =True ),'M 5-5 5-2 7-4 7-5 9-5 9-3 8-3 5 0 7 2 7-1 9-1 9 9 7 9 7 8 5 6 5 9 3 9 3 5 0 5-3 8-3 9-5 9-5 7-4 7-2 5-5 5-5 2-7 4-7 5-9 5-9 3-8 3-5 0-8-3-9-3-9-5-6-5-8-7-9-7-9-9-7-9-7-8-4-5zM 0 3 1 2 0 1-1 2zM 4 1 3 2 4 3 6 3zM-5-3-6-3-5-2zM 7 6 7 5 6 5z'))
