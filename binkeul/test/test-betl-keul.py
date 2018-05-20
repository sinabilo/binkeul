from nose .tools import *
from __head import ClsTest ,godir ,getsatic
from binkeul .betl .keul import Keul
from binkeul .betl .bkode import BKode
import tempfile ,filecmp
import os
class TestSuite (ClsTest ):
	def setUp (self ):
		self .ke1 =Keul ([6561 ,111212 ,22123 ,344384 ,55454554 ,65543 ,112 ,323 ,4 ,45 ])
		self .ke2 =Keul ([BKode (1401686504 ),BKode (1366480936 ),BKode (1412908020 ),BKode (1302229480 ),BKode (1459664628 ),BKode (1303638944 ),BKode (1280295712 ),BKode (1334270112 ),BKode (345129440 ),BKode (1401686508 ),BKode (97230048 ),BKode (2081263416 ),BKode (1275166768 ),BKode (1073856960 ),BKode (1491831256 ),BKode (1829133228 ),BKode (1920163588 ),BKode (1326868720 ),BKode (261679236 ),BKode (631495024 ),BKode (1174823008 ),BKode (1594053152 ),BKode (110336128 ),BKode (1073766096 ),BKode (1277065696 ),BKode (1138294964 ),BKode (1804431492 ),BKode (1301266608 ),BKode (1160515704 ),BKode (1630103848 )])
	def test_Keul_01 (self ):
		eq_ (repr (self .ke1 ),"Keul('PewEAWRCEarydEAqYYEcpwDObZEdEa...')")
		eq_ (repr (self .ke2 ),"Keul('oqGvPIWlSveqUQUvSXyiGVlYTEUWGi...')")
