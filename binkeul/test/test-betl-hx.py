from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .hx import HxSet ,HxOrd
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		self .bits1 ='0011000110001100001000000100000000000000001001000000000000011000000001010100001111010101011010001'
		self .hxs1 =HxSet (self .bits1 )
	def test_Hx_01 (self ):
		eq_ (str (self .hxs1 ),self .bits1 )
	def test_Hx_02 (self ):
		import json
		def make_uvkord ():
			UvkOrd ={}
			import json
			for i ,hx in enumerate (HxOrd ):
				UvkOrd [hx .uvk ]=i
			return UvkOrd
		UvkOrd_ ={"55P":0 ,"64L":1 ,"64R":2 ,"65T":3 ,"75P":4 ,"74T":5 ,"73P":6 ,"63T":7 ,"66L":8 ,"66R":9 ,"76T":10 ,"77P":11 ,"67T":12 ,"57P":13 ,"56T":14 ,"54T":15 ,"53P":16 ,"43T":17 ,"33P":18 ,"34T":19 ,"44R":20 ,"44L":21 ,"47T":22 ,"37P":23 ,"36T":24 ,"35P":25 ,"45T":26 ,"46R":27 ,"46L":28 ,"42L":29 ,"42R":30 ,"32T":31 ,"31P":32 ,"41T":33 ,"62L":34 ,"62R":35 ,"52T":36 ,"51P":37 ,"61T":38 ,"82L":39 ,"82R":40 ,"72T":41 ,"71P":42 ,"81T":43 ,"91P":44 ,"92T":45 ,"84L":46 ,"84R":47 ,"83T":48 ,"93P":49 ,"94T":50 ,"86L":51 ,"86R":52 ,"85T":53 ,"95P":54 ,"96T":55 ,"88L":56 ,"88R":57 ,"87T":58 ,"97P":59 ,"98T":60 ,"99P":61 ,"89T":62 ,"21T":63 ,"11P":64 ,"12T":65 ,"13P":66 ,"23T":67 ,"22R":68 ,"22L":69 ,"14T":70 ,"15P":71 ,"25T":72 ,"24R":73 ,"24L":74 ,"16T":75 ,"17P":76 ,"27T":77 ,"26R":78 ,"26L":79 ,"18T":80 ,"19P":81 ,"29T":82 ,"39P":83 ,"38T":84 ,"28R":85 ,"28L":86 ,"49T":87 ,"59P":88 ,"58T":89 ,"48R":90 ,"48L":91 ,"69T":92 ,"79P":93 ,"78T":94 ,"68R":95 ,"68L":96 }
		eq_ (UvkOrd_ ,make_uvkord ())
	def test_Hx_03 (self ):
		za1 =self .hxs1 .toZ3a2s ()
		hxs2 =HxSet .fromZ3a2s (za1 )
		bts2 =hxs2 .bitset
		eq_ (self .bits1 ,bts2 )
