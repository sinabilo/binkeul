import random ,pdb ,collections ,enum ,functools
from binkeul .betl .hx import HxOrd ,HxSet
class Fo (enum .Enum ):
	NONE =-1
	DI =lambda x :(32 |64 )&x .value
	I =32
	IM =32 |16
	IE =32 |3
	D =64
	DL =64 |1
	DR =64 |2
	DT =64 |12
	DV =64 |4
	DH =64 |8
	DP =64 |16
	G =128
	W =0
	WL =0 |1
	WR =0 |2
	WV =0 |4
	WH =0 |8
	WP =0 |16
	def __and__ (self ,other ):
		return Fo (self ._check_none (self .value &other .value ))
	def __or__ (self ,other ):
		return Fo (self ._check_none (self .value |other .value ))
	def __xor__ (self ,other ):
		return Fo (self ._check_none (self .value ^other .value ))
	def _check_none (self ,val ):
		try :return Fo (val )
		except :return Fo (-1 )
class Foint :
	def __init__ (self ,x ,y ,k =None ):
		try :
			assert self .valid_xyk (x ,y ,k )
		except :
			raise ValueError ("Foint({},{},{}) invalid !!".format (x ,y ,k ))
		self .__data =(x ,y ,k )
	@classmethod
	def setMapFromHx (cls ,hxord ):
		dic ={}
		for i ,hx in enumerate (hxord ):
			if hx .k =="T":
				k =Fo .DH if hx .u %2 else Fo .DV
			else :
				k ={"P":Fo .DP ,"R":Fo .DR ,"L":Fo .DL }[hx .k ]
			fo =cls (hx .u ,hx .v ,k )
			dic [fo ]=i
		return dic
	@property
	def x (self ):return self .__data [0 ]
	@property
	def y (self ):return self .__data [1 ]
	@property
	def xy (self ):return (self .__data [0 ],self .__data [1 ])
	@property
	def k (self ):return self .__data [2 ]
	def tuple (self ):
		return self .__data
	def __repr__ (self ):
		return "Foint{}".format (self .tuple ())
	def __hash__ (self ):
		return hash (self .tuple ())
	def __eq__ (self ,other ):
		return self .tuple ()==other .tuple ()
	def kind (self ):
		return self .k
	def __sub__ (self ,other ):
		return Foint (self .x -other .x ,self .y -other .y ,None )
	def __abs__ (self ):
		return Foint (abs (self .x ),abs (self .y ),None )
	@staticmethod
	def valid_xyk (x ,y ,k ):
		if k ==None :
			return True
		elif k in (Fo .IE ,Fo .DL ,Fo .DR ,Fo .WL ,Fo .WR ):
			if x %2 ==y %2 ==1 :
				return True
		elif k in (Fo .IM ,Fo .DP ,Fo .WP ):
			if x %2 ==y %2 ==0 :
				return True
		elif k in (Fo .DH ,Fo .DV ,Fo .WH ,Fo .WV ):
			x_ =x %2
			y_ =y %2
			if (x_ *y_ )==0 and (x_ +y_ )==1 :
				return True
		return False
FoOrdMap =Foint .setMapFromHx (HxOrd )
OrdFoMap ={v :k for k ,v in FoOrdMap .items ()}
class FodrawStack (list ):
	undomax =10
	def __init__ (self ,kode =None ):
		super ().__init__ ()
		self .__redo =[]
		if kode :
			self .addKode (kode )
	def addItem (self ,item ):
		assert isinstance (item ,set )
		if self .undomax ==len (self ):
			new_i0 =self .__snapshot (start =0 ,end =2 )
			i0 =self .pop (0 )
			self [0 ]=new_i0
		elif self .undomax <len (self ):
			raise ValueError ("Fodraw 의 갯수는 10 이하여야 함")
		self .append (item )
		self .__redo .clear ()
	def addKode (self ,kode ):
		fod =Fodata .fromHxs (kode .getHxs ())
		fow =Fodraw .fromFoD (fod )
		self .addItem (fow )
	def undo (self ):
		if len (self )>0 :
			self .__redo .append (self .pop ())
	def redo (self ):
		if len (self .__redo )>0 :
			self .append (self .__redo .pop ())
	def __snapshot (self ,end =None ,start =0 ):
		'''
        '''
		if len (self [start :end ])>0 :
			return Fodraw (functools .reduce (lambda x ,y :x ^y ,self [start :end ]))
		else :
			return Fodraw ()
	def head (self ):
		return self .__snapshot (start =-1 )
	def body (self ):
		return self .__snapshot (start =0 ,end =-1 )
	def allw (self ):
		return self .__snapshot (start =0 ,end =None )
	def getFoGD (self ):
		fod =self .allw ().getFoD ()
		fog =self .allw ().getAreaG ()
		return fod ,fog
	def sumw (self ):
		if len (self )>0 :
			return Fodraw (functools .reduce (lambda x ,y :x |y ,self ))
		else :
			return Fodraw ()
	def __repr__ (self ):
		return "FodrawStack({})".format (super ().__repr__ ())
class FoH1 (int ):
	def __new__ (cls ,val ):
		assert 0 <=val <65536
		return super ().__new__ (cls ,val )
class FoL3 (int ):
	def __new__ (cls ,val ):
		assert 0 <=val <158456325028528675187087900672
		return super ().__new__ (cls ,val )
class Fodata (set ):
	def __init__ (self ,ls =[]):
		super ().__init__ (ls )
	def getFoW (self ):
		pass
	def __hash__ (self ):
		return hash (frozenset (self ))
	def nearXys (self ):
		xys =set ()
		for fo in self :
			xys .add (fo .xy )
			if fo .k ==Fo .DP :
				xys .add ((fo .x -1 ,fo .y ))
				xys .add ((fo .x +1 ,fo .y ))
				xys .add ((fo .x ,fo .y -1 ))
				xys .add ((fo .x ,fo .y +1 ))
			elif fo .k ==Fo .DH :
				xys .add ((fo .x +1 ,fo .y ))
				xys .add ((fo .x -1 ,fo .y ))
			elif fo .k ==Fo .DV :
				xys .add ((fo .x ,fo .y -1 ))
				xys .add ((fo .x ,fo .y +1 ))
			elif fo .k ==Fo .DR :
				xys .add ((fo .x -1 ,fo .y -1 ))
				xys .add ((fo .x +1 ,fo .y +1 ))
			elif fo .k ==Fo .DL :
				xys .add ((fo .x -1 ,fo .y +1 ))
				xys .add ((fo .x +1 ,fo .y -1 ))
		return xys
	def getHxs (self ):
		return HxSet ([FoOrdMap [fo ]for fo in self ])
	@classmethod
	def fromHxs (cls ,hxs ):
		return Fodata ([OrdFoMap [ord ]for ord in hxs ])
class Fodraw (set ):
	def __init__ (self ,ls =[]):
		super ().__init__ (ls )
	def update (self ,a ):
		a .discard (None )
		super ().update (a )
		self .deleteWP ()
	def add (self ,a ):
		if not a :return
		super ().add (a )
		self .deleteWP ()
	@classmethod
	def fromFoD (cls ,fod ):
		fos =[]
		dps =set ()
		for d in fod :
			if d .k in (Fo .DL ,Fo .DR ,Fo .DH ,Fo .DV ):
				fos .append (Foint (d .x ,d .y ,d .k ^Fo .D ))
			else :
				dps .add (d )
		foo_set =Fodata ()
		for d in fos :
			foo_set .update (Fodraw .w2d (d ))
		ddps =set (filter (lambda i :i .k ==Fo .DP ,foo_set ))
		fos +=[Foint (p .x ,p .y ,Fo .WP )for p in (ddps ^dps )]
		return Fodraw (fos )
	def getFoD (self ,xor =True ):
		foo_set =Fodata ()
		for d in filter (lambda i :i .k !=Fo .WP ,self ):
			foo_set .update (Fodraw .w2d (d ))
		for d in filter (lambda i :i .k ==Fo .WP ,self ):
			rd =set (Fodraw .w2d (d ))
			if xor :foo_set ^=rd
			else :foo_set |=rd
		return foo_set
	def getAreaG (self ):
		fod =self .getFoD ()
		if not fod :
			return Fodata ()
		near_xys =fod .nearXys ()
		xmin =ymin =4
		xmax =ymax =-4
		xs =[fo .x for fo in fod ]
		ys =[fo .y for fo in fod ]
		xmin ,xmax =min (xs ),max (xs )
		ymin ,ymax =min (ys ),max (ys )
		if xmin ==xmax :
			xmin -=1
			xmax +=1
		if ymin ==ymax :
			ymin -=1
			ymax +=1
		fo_list =[]
		for fo ,idx in FoOrdMap .items ():
			if xmin <=fo .x <=xmax and ymin <=fo .y <=ymax :
				if fo .xy in near_xys :
					fo_list .append (fo )
		return Fodata (fo_list )
	@staticmethod
	def w2d (w ):
		if w .k ==Fo .WP :
			return [Foint (w .x ,w .y ,Fo .DP )]
		elif w .k ==Fo .WL :
			return [
			Foint (w .x +1 ,w .y -1 ,Fo .DP ),
			Foint (w .x ,w .y ,Fo .DL ),
			Foint (w .x -1 ,w .y +1 ,Fo .DP ),
			]
		elif w .k ==Fo .WR :
			return [
			Foint (w .x -1 ,w .y -1 ,Fo .DP ),
			Foint (w .x ,w .y ,Fo .DR ),
			Foint (w .x +1 ,w .y +1 ,Fo .DP ),
			]
		elif w .k ==Fo .WH :
			return [
			Foint (w .x -1 ,w .y ,Fo .DP ),
			Foint (w .x ,w .y ,Fo .DH ),
			Foint (w .x +1 ,w .y ,Fo .DP ),
			]
		elif w .k ==Fo .WV :
			return [
			Foint (w .x ,w .y -1 ,Fo .DP ),
			Foint (w .x ,w .y ,Fo .DV ),
			Foint (w .x ,w .y +1 ,Fo .DP ),
			]
	def backspace (self ):
		pass
	def deleteWP (self ):
		if len (self )>1 :
			for d in self :
				if d .k ==Fo .WP :
					self .remove (d )
					return d
class FoInputs (list ):
	pass
class FoEInputs (FoInputs ):
	pass
class FoMInputs (FoInputs ):
	def __init__ (self ,fopad ):
		super ().__init__ ([])
		self .fopad =fopad
		self .foscene =fopad .foscene
		self .fodraw_stack =fopad .fodraw_stack
		self .fodraw =Fodraw ()
		self .cur =0
		self .endtype =None
	def appendFilter (self ,fo ):
		if len (self )==0 :
			if fo .k ==Fo .IM :
				self .pushFoI (fo )
			else :
				return
		if fo .k ==Fo .IM :
			if self [-1 ].k ==Fo .IE :
				diff_1 =self [-1 ]-fo
				diff_2 =self [-2 ]-self [-1 ]
				if diff_1 ==diff_2 :
					self .pushFoI (fo )
				else :
					self .popFoI ()
			elif self [-1 ].k ==Fo .IM :
				diff =abs (self [-1 ]-fo )
				if (diff .x *diff .y ==0 )and (diff .x +diff .y ==2 ):
					self .pushFoI (fo )
		elif fo .k ==Fo .IE :
			diff =abs (self [-1 ]-fo )
			if diff .x ==diff .y ==1 :
				self .pushFoI (fo )
	def pushFoI (self ,fo ):
		self .foscene .foidic [fo ].setSelected (True )
		self .foscene .foidic [fo ].setHover (True )
		super ().append (fo )
		self .fodraw .add (self .i2w ())
		self .showFoD ()
		return None
	def popFoI (self ):
		fo =self [-1 ]
		r =super ().pop ()
		if not fo in self :
			self .foscene .foidic [fo ].setSelected (False )
			self .foscene .foidic [fo ].setHover (False )
		return r
	def append (self ,cfo ):
		if len (self )>0 :
			pfo =self [-1 ]
			self .foscene .foidic [pfo ].setHover (False )
		return self .appendFilter (cfo )
	def appendEnd (self ):
		if len (self )>0 :
			self .endtype =self [-1 ].k
			if self .endtype ==Fo .IE :
				self .pop ()
		self .fodraw_stack .addItem (self .fodraw )
		if len (self )>0 :
			for i in self .foscene .foidic .values ():
				i .setSelected (False )
		super ().clear ()
	def getFoW (self ):
		return self .fodraw
	def showFoD (self ):
		if self [-1 ].k ==Fo .IE :return
		for o in self .fodraw .getFoD ():
			self .foscene .foddic [o ].show ()
			self .foscene .foddic [o ].setSelected (True )
	def i2w (self ):
		if len (self )<1 :
			return None
		foi_1 =self [-1 ]
		if len (self )==1 :
			return Foint (foi_1 .x ,foi_1 .y ,Fo .WP )
		else :
			foi_2 =self [-2 ]
			if foi_2 .k ==Fo .IE and foi_1 .k ==Fo .IM :
				foi_3 =self [-3 ]
				rr =(foi_3 .x -foi_1 .x ==foi_3 .y -foi_1 .y )
				return Foint (
				foi_2 .x ,
				foi_2 .y ,
				Fo .WR if rr else Fo .WL )
			elif foi_2 .k ==Fo .IM and foi_1 .k ==Fo .IM :
				return Foint (
				(foi_2 .x +foi_1 .x )//2 ,
				(foi_2 .y +foi_1 .y )//2 ,
				Fo .WH if (foi_2 .x -foi_1 .x )else Fo .WV
				)
			else :
				return None
