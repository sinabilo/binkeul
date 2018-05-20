import struct
from ctypes import Structure ,c_int32
from binkeul .betl .hxza import HxBaseZ3a2 ,HxBitsetRe
from binkeul .betl .pubcls import Rect ,Sz
class Hx (Structure ):
	_fields_ =[
	("u",c_int32 ,8 ),
	("v",c_int32 ,8 ),
	("_k",c_int32 ,8 ),
	("idx",c_int32 ,8 ),
	]
	all ={}
	ktype =tuple ("TPLR")
	def __new__ (cls ,u ,v ,k ,idx =None ):
		if (u ,v ,k )in cls .all :
			return cls .all [u ,v ,k ]
		obj =super ().__new__ (cls )
		cls .all [u ,v ,k ]=obj
		return obj
	def __init__ (self ,u ,v ,k ,idx =None ):
		if idx ==None :return
		super ().__init__ ()
		if not (idx ==-1 ):
			assert (-5 <u <5 )and (-5 <v <5 )
		assert k in self .ktype
		if k =="P":
			assert u %2 ==v %2 ==0
		elif k =='T':
			assert (u %2 +v %2 )==1
		elif k in ('R','L'):
			assert u %2 ==v %2 ==1
		else :
			raise UserWarning
		self .u =u
		self .v =v
		self ._k =self .ktype .index (k )
		self .idx =idx
	def __hash__ (self ):
		return hash ((self .u ,self .v ,self ._k ))
	@property
	def rect (self ):
		top =self .u *2
		left =self .v *2
		return (x -1 ,y -1 ,2 ,2 )
	@property
	def uvk (self ):
		return "{}{}{}".format (self .u +5 ,self .v +5 ,self .k )
	@property
	def x (self ):return (self .u *2 )
	@property
	def y (self ):return (self .v *2 )
	@property
	def kxy (self ):
		return "{}{:0>2}{:0>2}".format (self .k .lower (),self .x +9 ,self .y +9 )
	@staticmethod
	def fromUvk (kuv ):
		return Uvk (int (kuv [1 ])-5 ,int (kuv [2 ])-5 ,kuv [0 ].upper ())
	@property
	def k (self ):
		return self .ktype [self ._k ]
	def getval (self ):
		return struct .unpack ('L',self )[0 ]
	def gettuple (self ):
		return self .u ,self .v ,self .k ,self .idx
	def __iter__ (self ):
		return iter (self .gettuple ())
	def getroll (self ,u ,v ):
		assert u %2 ==v %2 ==0
		assert (-5 <u <5 )and (-5 <v <5 )
		u =self .u +u
		v =self .v +v
		if u <-4 :u %=4
		elif u >4 :u %=-4
		if v <-4 :v %=4
		elif v >4 :v %=-4
		return Uvk (u ,v ,self .k )
	def getmove (self ,u ,v ):
		assert u %2 ==v %2 ==0
		u =self .u +u
		v =self .v +v
		u =struct .unpack ('b',c_int8 (u ))[0 ]
		v =struct .unpack ('b',c_int8 (v ))[0 ]
		return Uvk (u ,v ,self .k ,True )
	def getxofs (self ,cen_u ,cen_v ):
		u ,v =-cen_u ,-cen_v
		if (u in (-2 ,0 ,2 ))and (v in (-2 ,0 ,2 )):
			uvk2 =self .getmove (u ,v )
		elif (u in (-4 ,4 ))or (v in (-4 ,4 )):
			uvk2 =self .getroll (u ,v )
		else :
			raise UserWarning
		if uvk2 .iscore ():
			return uvk2
		return None
	def iscore (self ):
		if (-3 <self .u <3 )and (-3 <self .v <3 ):
			return True
		return False
	def __repr__ (self ):
		return "Hx{}".format (self .gettuple ())
class HxSet (set ):
	def __init__ (self ,hxs =[]):
		if isinstance (hxs ,(list ,tuple ,set )):
			super ().__init__ (hxs )
		elif isinstance (hxs ,str ):
			assert HxBitsetRe .match (hxs )
			hxlist =[]
			for i ,hx in enumerate (reversed (hxs )):
				if hx =="1":
					hxlist .append (i )
			super ().__init__ (hxlist )
		else :
			raise ValueError ()
	def __str__ (self ):
		return self .bitset
	@property
	def bitset (self ):
		blist =[]
		for i in range (97 ):
			blist .append ("1"if i in self else "0")
		return "".join (reversed (blist ))
	@property
	def bitnum (self ):
		return int (self .bitset ,2 )
	def gen (self ):
		for i in self :
			yield HxOrd [i ]
	@property
	def rect (self ):
		min_y =min_x =9
		max_y =max_x =-9
		for hx in self .gen ():
			if hx .k in ('P','T'):
				min_x =min (min_x ,hx .x -1 )
				max_x =max (max_x ,hx .x +1 )
				min_y =min (min_y ,hx .y -1 )
				max_y =max (max_y ,hx .y +1 )
			else :
				min_x =min (min_x ,hx .x -2 )
				max_x =max (max_x ,hx .x +2 )
				min_y =min (min_y ,hx .y -2 )
				max_y =max (max_y ,hx .y +2 )
		rt =Rect (min_x ,min_y ,max_x ,max_y )
		return rt .mgRect (Sz (1 ,1 ))
	def getBx (self ):
		Bx =0
		for hx in self :
			Bx ^=1 <<HxMap [hx ]
		return Bx
	def add (self ,hx ):
		if isinstance (hx ,int ):
			super ().update ([HxOrd (hx )])
		elif isinstance (hx ,Hx ):
			if hx .idx >-1 :
				super ().update ([hx .idx ])
		else :
			raise ValueError ()
	def toZ3a2s (self ):
		return HxBaseZ3a2 .encode (self .bitset )
	@staticmethod
	def fromZ3a2s (za ):
		return HxSet (HxBaseZ3a2 .decode (za ))
HxMap ={0 :28 ,1 :27 ,2 :26 ,3 :25 ,4 :24 ,5 :23 ,6 :22 ,7 :21 ,8 :20 ,9 :19 ,10 :18 ,11 :17 ,12 :16 ,13 :15 ,14 :14 ,15 :13 ,16 :12 ,17 :11 ,18 :10 ,19 :9 ,20 :8 ,21 :7 ,22 :6 ,23 :5 ,24 :4 ,25 :3 ,26 :2 ,27 :1 ,28 :0 ,29 :8 ,30 :7 ,31 :2 ,32 :3 ,33 :4 ,34 :1 ,35 :0 ,36 :2 ,37 :3 ,38 :9 ,39 :8 ,40 :7 ,41 :28 ,42 :10 ,43 :9 ,44 :10 ,45 :11 ,46 :26 ,47 :27 ,48 :13 ,49 :12 ,50 :11 ,51 :8 ,52 :7 ,53 :13 ,54 :12 ,55 :21 ,56 :26 ,57 :27 ,58 :28 ,59 :22 ,60 :21 ,61 :22 ,62 :23 ,63 :4 ,64 :5 ,65 :6 ,66 :5 ,67 :28 ,68 :0 ,69 :1 ,70 :6 ,71 :15 ,72 :14 ,73 :20 ,74 :19 ,75 :16 ,76 :15 ,77 :14 ,78 :0 ,79 :1 ,80 :16 ,81 :17 ,82 :18 ,83 :17 ,84 :28 ,85 :20 ,86 :19 ,87 :18 ,88 :24 ,89 :25 ,90 :27 ,91 :26 ,92 :23 ,93 :24 ,94 :25 ,95 :20 ,96 :19 }
__HxOrd =((0 ,0 ,'P'),
(1 ,-1 ,'L'),
(1 ,-1 ,'R'),
(1 ,0 ,'T'),
(2 ,0 ,'P'),
(2 ,-1 ,'T'),
(2 ,-2 ,'P'),
(1 ,-2 ,'T'),
(1 ,1 ,'L'),
(1 ,1 ,'R'),
(2 ,1 ,'T'),
(2 ,2 ,'P'),
(1 ,2 ,'T'),
(0 ,2 ,'P'),
(0 ,1 ,'T'),
(0 ,-1 ,'T'),
(0 ,-2 ,'P'),
(-1 ,-2 ,'T'),
(-2 ,-2 ,'P'),
(-2 ,-1 ,'T'),
(-1 ,-1 ,'R'),
(-1 ,-1 ,'L'),
(-1 ,2 ,'T'),
(-2 ,2 ,'P'),
(-2 ,1 ,'T'),
(-2 ,0 ,'P'),
(-1 ,0 ,'T'),
(-1 ,1 ,'R'),
(-1 ,1 ,'L'),
(-1 ,-3 ,'L'),
(-1 ,-3 ,'R'),
(-2 ,-3 ,'T'),
(-2 ,-4 ,'P'),
(-1 ,-4 ,'T'),
(1 ,-3 ,'L'),
(1 ,-3 ,'R'),
(0 ,-3 ,'T'),
(0 ,-4 ,'P'),
(1 ,-4 ,'T'),
(3 ,-3 ,'L'),
(3 ,-3 ,'R'),
(2 ,-3 ,'T'),
(2 ,-4 ,'P'),
(3 ,-4 ,'T'),
(4 ,-4 ,'P'),
(4 ,-3 ,'T'),
(3 ,-1 ,'L'),
(3 ,-1 ,'R'),
(3 ,-2 ,'T'),
(4 ,-2 ,'P'),
(4 ,-1 ,'T'),
(3 ,1 ,'L'),
(3 ,1 ,'R'),
(3 ,0 ,'T'),
(4 ,0 ,'P'),
(4 ,1 ,'T'),
(3 ,3 ,'L'),
(3 ,3 ,'R'),
(3 ,2 ,'T'),
(4 ,2 ,'P'),
(4 ,3 ,'T'),
(4 ,4 ,'P'),
(3 ,4 ,'T'),
(-3 ,-4 ,'T'),
(-4 ,-4 ,'P'),
(-4 ,-3 ,'T'),
(-4 ,-2 ,'P'),
(-3 ,-2 ,'T'),
(-3 ,-3 ,'R'),
(-3 ,-3 ,'L'),
(-4 ,-1 ,'T'),
(-4 ,0 ,'P'),
(-3 ,0 ,'T'),
(-3 ,-1 ,'R'),
(-3 ,-1 ,'L'),
(-4 ,1 ,'T'),
(-4 ,2 ,'P'),
(-3 ,2 ,'T'),
(-3 ,1 ,'R'),
(-3 ,1 ,'L'),
(-4 ,3 ,'T'),
(-4 ,4 ,'P'),
(-3 ,4 ,'T'),
(-2 ,4 ,'P'),
(-2 ,3 ,'T'),
(-3 ,3 ,'R'),
(-3 ,3 ,'L'),
(-1 ,4 ,'T'),
(0 ,4 ,'P'),
(0 ,3 ,'T'),
(-1 ,3 ,'R'),
(-1 ,3 ,'L'),
(1 ,4 ,'T'),
(2 ,4 ,'P'),
(2 ,3 ,'T'),
(1 ,3 ,'R'),
(1 ,3 ,'L'))
HxOrd =tuple (Hx (n [0 ],n [1 ],n [2 ],idx )for idx ,n in enumerate (__HxOrd ))
