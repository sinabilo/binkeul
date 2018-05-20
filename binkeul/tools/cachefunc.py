from functools import wraps
import shelve ,inspect ,pdb ,os
def fcached (dir =os .curdir ):
	def real_cached (func ):
		@wraps (func )
		def wrapper (*args ,**kws ):
			do_update =kws .pop ("cache_update",None )
			key =repr (args )+repr (kws )
			if do_update :
				func .cache .pop (key ,None )
			try :
				return func .cache [key ]
			except KeyError :
				func .cache [key ]=result =func (*args ,**kws )
				return result
		frm =inspect .stack ()[1 ]
		mod =inspect .getmodule (frm [0 ])
		shname =mod .__name__ +"."+func .__qualname__ +".shelve"
		func .cache =shelve .open (os .path .join (dir ,shname ))
		return wrapper
	return real_cached
import pickle
class PCache :
	def __init__ (self ,rootdir =None ):
		self .info ={}
		self .data ={}
		self .rootdir =rootdir
	def setfunc (self ,func_name ,func ):
		self .info [func_name ]=[func ,None ]
	def load (self ):
		if not os .path .isdir (self .rootdir ):
			os .mkdir (self .rootdir )
		for func_name ,(func ,_ )in self .info .items ():
			func_pickle =os .path .join (self .rootdir ,func_name +".pickle")
			self .info [func_name ][1 ]=func_pickle
			if os .path .isfile (func_pickle ):
				try :
					with open (func_pickle ,'rb')as f :
						func_cache =pickle .load (f )
				except :
					func_cache ={}
			else :
				func_cache ={}
			setattr (func ,"cache",func_cache )
			self .data [func_name ]=func_cache
	def dump (self ):
		if not self .rootdir :return
		for func_name ,(func ,func_pickle )in self .info .items ():
			with open (func_pickle ,'wb')as f :
				pickle .dump (self .data [func_name ],f )
	def deco (self ):
		return pcached (self )
def pcached (cacheObj =PCache ()):
	def real_cached (func ):
		@wraps (func )
		def wrapper (*args ,**kws ):
			key =args
			if kws .pop ("cache_update",None ):
				func .cache .pop (key ,None )
			assert len (kws )==0
			try :
				return func .cache [key ]
			except KeyError :
				func .cache [key ]=result =func (*args )
				return result
		frm =inspect .stack ()[1 ]
		mod =inspect .getmodule (frm [0 ])
		func_name =mod .__name__ +"."+func .__qualname__
		cacheObj .setfunc (func_name ,func )
		return wrapper
	return real_cached
