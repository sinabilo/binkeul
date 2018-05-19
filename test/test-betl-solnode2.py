from nose .tools import *
import __head
from binkeul .betl .solnode2 import *
from binkeul .betl .bkode import BKode
class TestSuite (__head .ClsTest ):
	def setUp (self ):
		pass
		codes =[
		[SOL_ROOT ,],
		[SOL_START ,BKode (1093540276 ),BKode (1292401072 )],
		[SOL_MID ,BKode (1168011696 )],
		[SOL_MID ,BKode (94418076 )],
		[SOL_ONE ,BKode (1292401072 )],
		[SOL_END ,BKode (1464588336 )],
		[SOL_START ,BKode (240088212 )],
		[SOL_MID ,BKode (261583088 )],
		[SOL_ONE ,BKode (1313775776 )],
		[SOL_MID ,BKode (1134220972 )],
		[SOL_END ,BKode (1920163588 )],
		[SOL_START ,BKode (1007507256 )],
		[SOL_MID ,BKode (1865030684 )],
		[SOL_MID ,BKode (1093540276 )],
		[SOL_END ,BKode (1168011696 )],
		[SOL_ONE ,BKode (94418076 )],
		]
		self .stree =makeSolTree (codes )
	def test_SOL_01 (self ):
		eq_ (self .stree .showTree (prt =False ),
		'''\
Kode(1,2): [BKode(1093540276), BKode(1292401072)]
Kode(2,2): [BKode(1168011696)]
Kode(2,2): [BKode(94418076)]
    Kode(0,2): [BKode(1292401072)]
Kode(3,2): [BKode(1464588336)]
    Kode(1,2): [BKode(240088212)]
    Kode(2,2): [BKode(261583088)]
        Kode(0,2): [BKode(1313775776)]
    Kode(2,2): [BKode(1134220972)]
    Kode(3,2): [BKode(1920163588)]
        Kode(1,2): [BKode(1007507256)]
        Kode(2,2): [BKode(1865030684)]
        Kode(2,2): [BKode(1093540276)]
        Kode(3,2): [BKode(1168011696)]
            Kode(0,2): [BKode(94418076)]
''')
	def test_SOL_02 (self ):
		eq_ (self .stree .childCount (),4 )
		eq_ (self .stree .child (2 ).childCount (),1 )
	def test_SOL_03 (self ):
		kl =self .stree .toKeul ()
		sol =SolItem .fromKeul (kl )
		eq_ (self .stree .showTree (),sol .showTree ())
