from nose .tools import *
import __head
from binkeul .betl .solnode import *
from binkeul .betl .bkode import BKode
class TestSuite (__head .ClsTest ):
	def setUp (self ):
		pass
		codes =[
		[SOL_ROOT ,],
		[SOL_START ,BKode (1093540276 ),BKode (1292401072 )],
		[SOL_MID ,BKode (1168011696 ),BKode (1464588336 )],
		[SOL_MID ,BKode (94418076 ),BKode (1920163588 )],
		[SOL_START ,BKode (1292401072 )],
		[SOL_END ,BKode (1292401072 )],
		[SOL_END ,BKode (1464588336 ),BKode (1093540276 )],
		[SOL_START ,BKode (240088212 )],
		[SOL_MID ,BKode (261583088 ),BKode (1920163588 ),BKode (1007507256 )],
		[SOL_ONE ,BKode (1313775776 ),BKode (1168011696 ),BKode (94418076 )],
		[SOL_MID ,BKode (1134220972 ),BKode (1464588336 )],
		[SOL_END ,BKode (1920163588 )],
		[SOL_START ,BKode (1007507256 ),BKode (261583088 )],
		[SOL_MID ,BKode (1865030684 ),BKode (1168011696 )],
		[SOL_MID ,BKode (1093540276 )],
		[SOL_END ,BKode (1168011696 ),BKode (261583088 ),BKode (1920163588 )],
		[SOL_ONE ,BKode (94418076 )],
		]
		self .stree =makeSolTree (codes )
	def test_SOL_01 (self ):
		eq_ (self .stree .showNodes (prt =False ),'''\
SolNode([SOL_START])
SolNode([SOL_MID])
SolNode([SOL_MID])
    SolNode([SOL_START])
    SolNode([SOL_END])
SolNode([SOL_END])
    SolNode([SOL_START])
    SolNode([SOL_MID])
        SolNode([SOL_ONE])
    SolNode([SOL_MID])
    SolNode([SOL_END])
        SolNode([SOL_START])
        SolNode([SOL_MID])
        SolNode([SOL_MID])
        SolNode([SOL_END])
            SolNode([SOL_ONE])
''')
		eq_ (self .stree .showTree (prt =False ),'''\
SolNode([SOL_START])
    SolData([BKode(1093540276), BKode(1292401072)])
SolNode([SOL_MID])
    SolData([BKode(1168011696), BKode(1464588336)])
SolNode([SOL_MID])
    SolData([BKode(94418076), BKode(1920163588)])
SolNode([SOL_START])
    SolData([BKode(1292401072)])
SolNode([SOL_END])
    SolData([BKode(1292401072)])
SolNode([SOL_END])
    SolData([BKode(1464588336), BKode(1093540276)])
SolNode([SOL_START])
    SolData([BKode(240088212)])
SolNode([SOL_MID])
    SolData([BKode(261583088), BKode(1920163588), BKode(1007507256)])
SolNode([SOL_ONE])
    SolData([BKode(1313775776), BKode(1168011696), BKode(94418076)])
SolNode([SOL_MID])
    SolData([BKode(1134220972), BKode(1464588336)])
SolNode([SOL_END])
    SolData([BKode(1920163588)])
SolNode([SOL_START])
    SolData([BKode(1007507256), BKode(261583088)])
SolNode([SOL_MID])
    SolData([BKode(1865030684), BKode(1168011696)])
SolNode([SOL_MID])
    SolData([BKode(1093540276)])
SolNode([SOL_END])
    SolData([BKode(1168011696), BKode(261583088), BKode(1920163588)])
SolNode([SOL_ONE])
    SolData([BKode(94418076)])
''')
	def test_SOL_02 (self ):
		import io ,pprint
		sio =io .StringIO ()
		pprint .pprint (self .stree .childItems ,stream =sio )
		sio .seek (0 )
		eq_ (sio .read (),'''\
[SolNode([SOL_START]),
 SolNode([SOL_MID]),
 SolNode([SOL_MID]),
 SolNode([SOL_START]),
 SolNode([SOL_END]),
 SolNode([SOL_END]),
 SolNode([SOL_START]),
 SolNode([SOL_MID]),
 SolNode([SOL_ONE]),
 SolNode([SOL_MID]),
 SolNode([SOL_END]),
 SolNode([SOL_START]),
 SolNode([SOL_MID]),
 SolNode([SOL_MID]),
 SolNode([SOL_END]),
 SolNode([SOL_ONE])]
''')
	def test_SOL_03 (self ):
		eq_ (self .stree .childCount (),16 )
		eq_ (self .stree .child (2 ).childCount (),1 )
		eq_ (self .stree .child (7 ).columnCount (),3 )
	def test_SOL_04 (self ):
		kl =self .stree .toKeul ()
		sol =SolNode .fromKeul (kl )
		eq_ (self .stree .showNodes (),sol .showNodes ())
	def test_SOL_05 (self ):
		ss =self .stree .child (2 ).serialize ()
		eq_ (ss ,[Kode (2 ,2 ),BKode (94418076 ),BKode (1920163588 ),Kode (1 ,2 ),BKode (1292401072 ),Kode (3 ,2 ),BKode (1292401072 )])
