from functools import lru_cache
from collections import deque
from binkeul .betl .pubcls import Po ,Rect
from binkeul .betl .hxpath import Vec
from binkeul .betl .ffc import Ffc ,FfcSet
class FfcPath :
	def __init__ (self ,ffcs ):
		assert isinstance (ffcs ,FfcSet )
		self .ffcs =ffcs
		self .cens =set ()
		self .vecs =set ()
		for ffc in ffcs .gen ():
			pos =FfcPos (ffc )
			self .cens .update (pos .cens )
			self .vecs .update (pos .genVecs ())
	def getActiveVecs (self ):
		vecs =[]
		for vec in self .vecs :
			if vec .getOppVec ()in self .vecs :
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
		vdir =deque ([(0 ,-1 ),(1 ,0 ),(0 ,1 ),(-1 ,0 )])
		vec_list =self .getActiveVecs ()
		polygon_group =[]
		while vec_list :
			vec =vec_list .pop (0 )
			start_p =vec .p1
			start_diff =vec .diff
			polygon =[start_p ]
			while True :
				vdir .rotate (4 -vdir .index (vec .dir ))
				vec ,addtrue =find_next_vec (vec ,vec_list ,vdir )
				if addtrue :polygon .append (vec .p1 )
				if vec .p2 ==start_p :
					break
			if simple and start_diff ==vec .diff :polygon .pop (0 )
			polygon_group .append (polygon )
		return polygon_group
	def getPathd (self ,simple =True ,rotate =False ):
		all =[]
		for polygon in self .getPolygons (simple ):
			if rotate :
				polygon =[Po (-y ,x )for x ,y in polygon ]
			x_ys =("{:2}{:2}".format (x ,y )for x ,y in polygon )
			all .append ("M"+"".join (x_ys )+"z")
		return "".join (all )
class FfcPos ():
	all =dict ()
	def __new__ (cls ,ffc ):
		if ffc in cls .all :
			return cls .all [ffc ]
		else :
			return super ().__new__ (cls )
	def __init__ (self ,ffc ):
		assert isinstance (ffc ,Ffc )
		if ffc in self .all :return
		self .ffc =ffc
		self .outline =None
		self .cens =None
		self .setupD ()
	def setupD (self ):
		x ,y =self .ffc .x ,self .ffc .y
		self .cens =[Po (x ,y )]
		self .outline =[
		Po (x -1 ,y -1 ),Po (x ,y -1 ),Po (x +1 ,y -1 ),
		Po (x +1 ,y ),
		Po (x +1 ,y +1 ),Po (x ,y +1 ),Po (x -1 ,y +1 ),
		Po (x -1 ,y )]
	def genVecs (self ):
		pos =self .outline
		last_po =pos [-1 ]
		pre_po =last_po
		for po in pos :
			yield Vec (pre_po ,po )
			pre_po =po
