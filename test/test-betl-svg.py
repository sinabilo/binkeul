from nose .tools import *
from __head import ClsTest ,godir ,getsatic ,tmfopen
from binkeul .betl .svg import KeulSvgFrm ,KodeSvgFrm
from binkeul .betl .keul import Keul
from binkeul .betl .bkode import BKode
from binkeul .betl .pubcls import SizeStyle ,Sz ,FixStyle
from binkeul .tools .svgimage import svgImage
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
		self .keul =Keul ([BKode (1401686504 ),BKode (1366480936 ),BKode (1412908020 ),BKode (1302229480 ),BKode (1459664628 ),BKode (1303638944 ),BKode (1280295712 ),BKode (1334270112 ),BKode (345129440 ),BKode (1401686508 ),BKode (97230048 ),BKode (2081263416 ),BKode (1275166768 ),BKode (1073856960 ),BKode (1491831256 ),BKode (1829133228 ),BKode (1920163588 ),BKode (1326868720 ),BKode (261679236 ),BKode (631495024 ),BKode (1174823008 ),BKode (1594053152 ),BKode (110336128 ),BKode (1073766096 ),BKode (1277065696 ),BKode (1138294964 ),BKode (1804431492 ),BKode (1301266608 ),BKode (1160515704 ),BKode (1630103848 )])
		svgconf ={
		"stroke-width":0 ,
		"stroke":'gray',
		"fill":'gray',
		}
		self .mk_hor =KeulSvgFrm (scale =2 ,svgconf =svgconf )
		self .mk_hor .layout .hor =True
		self .mk_hor .layout .space =Sz (2 ,10 )
		self .mk_hor .layout .limit =200
		self .mk_hor .layout .usedefs =True
		self .mk_ver =KeulSvgFrm (scale =2 ,svgconf =svgconf )
		self .mk_ver .layout .hor =False
		self .mk_ver .layout .space =Sz (10 ,2 )
		self .mk_ver .layout .limit =200
		self .mk_ver .layout .usedefs =True
	def test_Svg_01 (self ):
		with tmfopen (suffix ='.png')as tf :
			svg_bytes =self .mk_hor .make (self .keul )
			svgImage (svg_bytes ,tf )
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"mk_hor.png"))
	def test_Svg_02 (self ):
		with tmfopen (suffix ='.png')as tf :
			svg_bytes =self .mk_ver .make (self .keul )
			svgImage (svg_bytes ,tf )
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"mk_ver.png"))
	def test_Sdv_03 (self ):
		dwh =KodeSvgFrm (scale =3 ,fix =FixStyle .hor )
		with tmfopen (suffix ='.png')as tf :
			svg_bytes =dwh .draw (BKode (1168011696 ))
			svgImage (svg_bytes ,tf )
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"you-hor.png"))
	def test_Sdv_04 (self ):
		dwv =KodeSvgFrm (scale =3 ,fix =FixStyle .ver )
		with tmfopen (suffix ='.png')as tf :
			svg_bytes =dwv .draw (BKode (1168011696 ))
			svgImage (svg_bytes ,tf )
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"you-ver.png"))
	def test_Sdv_05 (self ):
		dw =KodeSvgFrm (scale =3 )
		with tmfopen (suffix ='.png')as tf :
			svg_bytes =dw .draw (BKode (1920163588 ))
			svgImage (svg_bytes ,tf )
			tf .close ()
			ok_ (filecmp .cmp (tf .name ,"flower.png"))
