from collections import namedtuple
from enum import Enum ,IntEnum ,auto
FixR =10
class FixStyle (IntEnum ):
	none =0
	ver =1
	hor =2
	square =3
class SizeStyle (Enum ):
	orign =auto ()
	pic1x =auto ()
	pic2x =auto ()
class Sz (namedtuple ("Space",["w","h"])):
	def __repr__ (self ):
		return "Sz({},{})".format (self .w ,self .h )
class Po (namedtuple ("Point",["x","y"])):
	def __repr__ (self ):
		return "Po({},{})".format (self .x ,self .y )
class Rect ():
	def __init__ (self ,left ,top ,right ,bottom ):
		self .left ,self .top ,self .right ,self .bottom =left ,top ,right ,bottom
	def __repr__ (self ):
		return "Rect({},{},{},{})".format (self .left ,self .top ,self .right ,self .bottom )
	def __iter__ (self ):
		for v in (self .left ,self .top ,self .right ,self .bottom ):
			yield v
	def __eq__ (self ,other ):
		if not isinstance (other ,Rect ):
			return False
		return tuple (self )==tuple (other )
	@property
	def width (self ):return self .right -self .left
	@property
	def height (self ):return self .bottom -self .top
	@property
	def size (self ):
		return Sz (self .width ,self .height )
	def fixRect (self ,fix =FixStyle .hor ,min =-FixR ,max =FixR ):
		import copy
		rt =copy .copy (self )
		if fix :
			if fix &FixStyle .ver :
				rt .left =min
				rt .right =max
			if fix &FixStyle .hor :
				rt .top =min
				rt .bottom =max
		return rt
	def mgRect (self ,mg ):
		return Rect (
		self .left -mg .w ,
		self .top -mg .h ,
		self .right +mg .w ,
		self .bottom +mg .h
		)
	def mvRect (self ,mv ):
		return Rect (
		self .left +mv .x ,
		self .top +mv .y ,
		self .right +mv .x ,
		self .bottom +mv .y
		)
	def scRect (self ,sc ):
		return Rect (
		self .left *sc ,
		self .top *sc ,
		self .right *sc ,
		self .bottom *sc
		)
