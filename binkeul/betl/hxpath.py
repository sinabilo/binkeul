from collections import deque ,namedtuple
from functools import lru_cache
from binkeul .base import fCached
from binkeul .betl .hx import Hx ,HxSet
from binkeul .betl .pubcls import Po ,Rect
class HxPath :
	def __init__ (self ,hxs =None ):
		self .hxs =HxSet ()
		self .cens =set ()
		self .vecs =set ()
		if hxs :
			if isinstance (hxs ,(list ,tuple ,set )):
				hxs =HxSet (hxs )
			self .update (hxs )
	def __eq__ (self ,other ):
		assert isinstance (other ,HxPath )
		return self .hxs ==other .hxs
	def __repr__ (self ):
		return "HxPath({})".format (set (self .hxs ))
	def resetRect (self ):
		xs ,ys =zip (*self .cens )
		self .left ,self .right =min (xs )-1 ,max (xs )+1
		self .top ,self .bottom =min (ys )-1 ,max (ys )+1
	@property
	def rect (self ):
		return Rect (self .left ,self .top ,self .right ,self .bottom )
	@property
	def mgrect (self ):
		return Rect (self .left -1 ,self .top -1 ,self .right +1 ,self .bottom +1 )
	@property
	def width (self ):return self .right -self .left
	@property
	def height (self ):return self .bottom -self .top
	def remove (self ,hxs ):
		self .hxs .difference_update (hxs )
		for hx in hxs .gen ():
			pos =HxPos (hx )
			self .cens .difference_update (pos .cens )
			self .vecs .difference_update (pos .genVecs ())
		self .resetRect ()
	def update (self ,hxs ):
		self .hxs .update (hxs )
		for hx in hxs .gen ():
			pos =HxPos (hx )
			self .cens .update (pos .cens )
			self .vecs .update (pos .genVecs ())
		self .resetRect ()
	def getActiveVecs (self ):
		vecs =[]
		for vec in self .vecs :
			if vec .getOppVec ()in self .vecs :
				continue
			if vec .iscontact (self .cens ):
				continue
			vecs .append (vec )
		return vecs
	def getPolygons (self ,simple =False ):
		def find_next_vec (vec ,vec_list ,vdir ):
			nextvec =min (
			(vdir .index (v .diff ),v )
			for v in filter (lambda v :v .p1 ==vec .p2 ,vec_list )
			)[1 ]
			vec_list .remove (nextvec )
			return nextvec ,(vec .diff !=nextvec .diff )if simple else True
		vdir =deque ([(-1 ,-1 ),(0 ,-1 ),(1 ,-1 ),(1 ,0 ),(1 ,1 ),(0 ,1 ),(-1 ,1 ),(-1 ,0 )])
		vec_list =self .getActiveVecs ()
		polygon_group =[]
		while vec_list :
			vec =vec_list .pop (0 )
			start_p =vec .p1
			start_diff =vec .diff
			polygon =[start_p ]
			while True :
				vdir .rotate (8 -vdir .index (vec .dir ))
				vec ,addtrue =find_next_vec (vec ,vec_list ,vdir )
				if addtrue :polygon .append (vec .p1 )
				if vec .p2 ==start_p :
					break
			if simple and start_diff ==vec .diff :polygon .pop (0 )
			polygon_group .append (polygon )
		return polygon_group
	def getPathd (self ,simple =False ):
		return self .__getPathd (simple )
	@fCached ()
	def __getPathd (self ,simple ):
		all =[]
		for polygon in self .getPolygons (simple ):
			x_ys =("{:2}{:2}".format (x ,y )for x ,y in polygon )
			all .append ("M"+"".join (x_ys )+"z")
		return "".join (all )
class Vec (tuple ):
	def __new__ (cls ,p1 ,p2 ):
		return super ().__new__ (cls ,[p1 ,p2 ])
	def __repr__ (self ):
		return "Vec{}".format (super ().__repr__ ())
	def __init__ (self ,p1 ,p2 ):
		self .p1 ,self .p2 =p1 ,p2
		xi ,yi =p2 .x -p1 .x ,p2 .y -p1 .y
		if xi ==yi :
			self .cpoints =((p2 .x ,p1 .y ),)
		elif xi ==-yi :
			self .cpoints =((p1 .x ,p2 .y ),)
		else :
			self .cpoints =(p1 ,p2 )
		self .dir =(-xi ,-yi )
		self .diff =(xi ,yi )
	def getOppVec (self ):
		return Vec (self .p2 ,self .p1 )
	def iscontact (self ,cens ):
		for np in self .cpoints :
			if np in cens :
				return True
		else :
			return False
class HxPos ():
	all =dict ()
	def __new__ (cls ,hx ):
		if hx in cls .all :
			return cls .all [hx ]
		else :
			return super ().__new__ (cls )
	def __init__ (self ,hx ):
		assert isinstance (hx ,Hx )
		if hx in self .all :return
		self .hx =hx
		self .outline =None
		self .cens =None
		if hx .k =='L':
			self .setupL ()
		elif hx .k =='R':
			self .setupR ()
		elif hx .k in "PT":
			self .setupPT ()
		self .all [hx ]=self
	def setupPT (self ):
		x ,y =self .hx .x ,self .hx .y
		self .cens =[Po (x ,y )]
		self .outline =[
		Po (x -1 ,y -1 ),Po (x ,y -1 ),Po (x +1 ,y -1 ),
		Po (x +1 ,y ),
		Po (x +1 ,y +1 ),Po (x ,y +1 ),Po (x -1 ,y +1 ),
		Po (x -1 ,y )]
	def setupL (self ):
		x ,y =self .hx .x ,self .hx .y
		x1 ,y1 ,x2 ,y2 =x -1 ,y +1 ,x +1 ,y -1
		self .cens =[Po (x1 ,y1 ),Po (x2 ,y2 )]
		self .outline =[
		Po (x1 ,y1 +1 ),Po (x1 -1 ,y1 +1 ),Po (x1 -1 ,y1 ),
		Po (x -1 ,y ),Po (x ,y -1 ),
		Po (x2 ,y2 -1 ),Po (x2 +1 ,y2 -1 ),Po (x2 +1 ,y2 ),
		Po (x +1 ,y ),Po (x ,y +1 )
		]
	def setupR (self ):
		x ,y =self .hx .x ,self .hx .y
		x1 ,y1 ,x2 ,y2 =x -1 ,y -1 ,x +1 ,y +1
		self .cens =[Po (x1 ,y1 ),Po (x2 ,y2 )]
		self .outline =[
		Po (x1 -1 ,y1 ),Po (x1 -1 ,y1 -1 ),Po (x1 ,y1 -1 ),
		Po (x ,y -1 ),Po (x +1 ,y ),
		Po (x2 +1 ,y2 ),Po (x2 +1 ,y2 +1 ),Po (x2 ,y2 +1 ),
		Po (x ,y +1 ),Po (x -1 ,y )
		]
	def genVecs (self ):
		pos =self .outline
		last_po =pos [-1 ]
		pre_po =last_po
		for po in pos :
			yield Vec (pre_po ,po )
			pre_po =po
