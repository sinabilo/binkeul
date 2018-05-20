__version__ ='0.5.1'
__author__ ='David Townshend'
__all__ =['undoable','group','Stack','stack','setstack']
import contextlib
from collections import deque
class MethodName (str ):
	def __new__ (cls ,st ,isdo =None ):
		return super ().__new__ (cls ,st )
	def __init__ (self ,st ,isdo =None ):
		self .isdo =isdo
class _Action :
	def __init__ (self ,generator ,args ,kwargs ,obj =None ):
		self ._generator =generator
		self .args =args
		self .kwargs =kwargs
		self .obj =obj
		self ._text =''
	def callback_iters (self ,isdo =True ):
		if self .obj !=None and hasattr (self .obj ,"callbacks"):
			method_name =MethodName (self .method_name ,isdo )
			return [iter (call (self .obj ,method_name ,self .args [1 :],self .kwargs ))for call in self .obj .callbacks ]
		else :
			return []
	def do (self ):
		'Do or redo the action'
		self ._runner =self ._generator (*self .args ,**self .kwargs )
		self .method_name =self ._runner .__name__
		iters =self .callback_iters (True )
		for callp in iters :
			next (callp )
		rets =next (self ._runner )
		for calln in iters :
			try :next (calln )
			except StopIteration :pass
		if isinstance (rets ,tuple ):
			self ._text =rets [0 ]
			return rets [1 :]
		elif rets is None :
			self ._text =''
			return None
		else :
			self ._text =rets
			return None
	def undo (self ):
		'Undo the action'
		iters =self .callback_iters (False )
		for callp in iters :
			next (callp )
		try :
			next (self ._runner )
		except StopIteration :
			pass
		for calln in iters :
			try :next (calln )
			except StopIteration :pass
		del self ._runner
	def text (self ):
		'Return the descriptive text of the action'
		return self ._text
def undoable (generator ):
	''' Decorator which creates a new undoable action type.
    This decorator should be used on a generator of the following format::
        @undoable
        def operation(*args):
            do_operation_code
            yield 'descriptive text'
            undo_operator_code
    '''
	def inner (*args ,**kwargs ):
		action =_Action (generator ,args ,kwargs )
		ret =action .do ()
		stack ().append (action )
		if isinstance (ret ,tuple ):
			if len (ret )==1 :
				return ret [0 ]
			elif len (ret )==0 :
				return None
		return ret
	return inner
def undomethod (generator ):
	def inner (*args ,**kwargs ):
		obj =args [0 ]
		action =_Action (generator ,args ,kwargs ,obj =obj )
		ret =action .do ()
		stack ().append (action )
		if isinstance (ret ,tuple ):
			if len (ret )==1 :
				return ret [0 ]
			elif len (ret )==0 :
				return None
		return ret
	return inner
class _Group :
	def __init__ (self ,desc ):
		self ._desc =desc
		self ._stack =[]
	def __enter__ (self ):
		stack ().setreceiver (self ._stack )
	def __exit__ (self ,exc_type ,exc_val ,exc_tb ):
		if exc_type is None :
			stack ().resetreceiver ()
			stack ().append (self )
		return False
	def undo (self ):
		for undoable in reversed (self ._stack ):
			undoable .undo ()
	def do (self ):
		for undoable in self ._stack :
			undoable .do ()
	def text (self ):
		return self ._desc .format (count =len (self ._stack ))
def group (desc ):
	return _Group (desc )
class Stack :
	def __init__ (self ):
		self ._undos =deque ()
		self ._redos =deque ()
		self ._receiver =self ._undos
		self ._savepoint =None
		self .undocallback =lambda :None
		self .docallback =lambda :None
	def canundo (self ):
		''' Return *True* if undos are available '''
		return len (self ._undos )>0
	def canredo (self ):
		''' Return *True* if redos are available '''
		return len (self ._redos )>0
	def redo (self ):
		''' Redo the last undone action.
        This is only possible if no other actions have occurred since the
        last undo call.
        '''
		if self .canredo ():
			undoable =self ._redos .pop ()
			with self ._pausereceiver ():
				try :
					undoable .do ()
				except :
					self .clear ()
					raise
				else :
					self ._undos .append (undoable )
			self .docallback ()
	def undo (self ):
		''' Undo the last action. '''
		if self .canundo ():
			undoable =self ._undos .pop ()
			with self ._pausereceiver ():
				try :
					undoable .undo ()
				except :
					self .clear ()
					raise
				else :
					self ._redos .append (undoable )
			self .undocallback ()
	def clear (self ):
		''' Clear the undo list. '''
		self ._undos .clear ()
		self ._redos .clear ()
		self ._savepoint =None
		self ._receiver =self ._undos
	def undocount (self ):
		''' Return the number of undos available. '''
		return len (self ._undos )
	def redocount (self ):
		''' Return the number of redos available. '''
		return len (self ._undos )
	def undotext (self ):
		''' Return a description of the next available undo. '''
		if self .canundo ():
			return ('Undo '+self ._undos [-1 ].text ()).strip ()
	def redotext (self ):
		''' Return a description of the next available redo. '''
		if self .canredo ():
			return ('Redo '+self ._redos [-1 ].text ()).strip ()
	@contextlib .contextmanager
	def _pausereceiver (self ):
		''' Return a contect manager which temporarily pauses the receiver. '''
		self .setreceiver ([])
		yield
		self .resetreceiver ()
	def setreceiver (self ,receiver =None ):
		''' Set an object to receiver commands pushed onto the stack.
        By default it is the internal stack, but it can be set (usually
        internally) to any object with an *append()* method.
        '''
		assert hasattr (receiver ,'append')
		self ._receiver =receiver
	def resetreceiver (self ):
		''' Reset the receiver to the internal stack.'''
		self ._receiver =self ._undos
	def append (self ,action ):
		''' Add a undoable to the stack, using ``receiver.append()``. '''
		if self ._receiver is not None :
			self ._receiver .append (action )
		if self ._receiver is self ._undos :
			self ._redos .clear ()
			self .docallback ()
	def savepoint (self ):
		''' Set the savepoint. '''
		self ._savepoint =self .undocount ()
	def haschanged (self ):
		''' Return *True* if the state has changed since the savepoint.
        This will always return *True* if the savepoint has not been set.
        '''
		return self ._savepoint is None or self ._savepoint !=self .undocount ()
_stack =None
def stack ():
	''' Return the currently used stack.
    If no stack has been set, a new one is created and set.
    '''
	global _stack
	if _stack is None :
		_stack =Stack ()
	return _stack
def setstack (stack ):
	''' Set the undo stack to a specific `Stack` object.'''
	global _stack
	_stack =stack
